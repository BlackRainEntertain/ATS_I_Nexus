import os, sys, json, time, asyncio, edge_tts, subprocess, re, shutil
from rich.console import Console
from rich.markup import escape
from datetime import datetime
import win32com.client  # Notfall-Ausweich-Kern

CURRENT_RAM_COUNT = 0  # Globaler Zähler im schnellen Arbeitsspeicher

os.system("title AUDIO_MASTER_BUTLER_V45.0_SPLIT_TITAN")
console = Console()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Q_DIR = os.path.join(BASE_DIR, "_Voice_Queue")
SAFE_DIR = os.path.join(BASE_DIR, "_Active_Ticket")
P_FILE = os.path.join(BASE_DIR, "NEXUS_PAUSE.tmp")
N_FILE = os.path.join(BASE_DIR, "NEXUS_NEXT.tmp")
CACHE_DIR = os.path.join(BASE_DIR, "_Audio_Cache")
LIMIT_FILE = os.path.join(BASE_DIR, "GEE_CONTEXT_LIMIT.txt")

for d in [SAFE_DIR, Q_DIR, CACHE_DIR]:
    if not os.path.exists(d): os.makedirs(d)


async def speak_and_wait(ticket):
    global CURRENT_RAM_COUNT  
    raw_cleaned = re.sub(r'[={}_#<>"]', ' ', ticket.get('text', ''))
    full_text = raw_cleaned.translate(str.maketrans("éèêëàâîïôûçÉÈÊËÀÂÎÏÔÛÇ", "eeeeaaiiouçEEEEAAIIOUC"))
    
    if "RESET_SIGNAL" in full_text: 
        return "FINISHED"


    owner_key = ticket.get('owner', 'UNKNOWN').upper()
    raw_sender = ticket.get('sender')
    display_name = (raw_sender if raw_sender else owner_key).upper()
    
    colors = {"GEE": "bright_blue", "NEXUS": "cyan", "META": "magenta", "ATSI": "bright_cyan", "GROK": "#FFEE00"}
    color = colors.get(owner_key, "white") 
    
    uhrzeit = datetime.now().strftime("%H:%M:%S")
    safe_preview = escape(full_text[:60].replace("\n", " "))

    # Alte Cache-Dateien dieses Owners aufräumen
    for f in os.listdir(CACHE_DIR):
        if f.startswith(f"voice_{owner_key}_") and f.endswith(".mp3"):
            try: os.remove(os.path.join(CACHE_DIR, f))
            except: pass

    # =======================================================================
    # ZENTRALE STIMMEN-ZUWEISUNG IM BUTLER (v45.4 - Stability & Smooth Audio)
    # =======================================================================
    single_voice = ticket.get('voice', 'de-DE-TanjaNeural')

    if owner_key == "BRE" and not ticket.get('voice_de'):
        voice_de = None
        voice_en = None
        single_voice = "en-US-AndrewMultilingualNeural"
        ticket['rate'] = "+4%"
        ticket['pitch'] = "+0Hz"
    elif owner_key == "BOOK_GEE" and not ticket.get('voice_de'):
        voice_de = "de-CH-LeniNeural"
        voice_en = "en-US-AvaNeural"
        rate_de, rate_en = "+9%", "-4%"
        pitch_de, pitch_en = "-2Hz", "-2Hz"
    else:
        voice_de = ticket.get('voice_de')
        voice_en = ticket.get('voice_en')
        rate_de  = ticket.get('rate_de', '+9%')
        rate_en  = ticket.get('rate_en', '-4%')
        pitch_de = ticket.get('pitch_de', '+2Hz')
        pitch_en = ticket.get('pitch_en', '-2Hz')

    use_split = bool(voice_de and voice_en)



    try:
        from pydub import AudioSegment
        from io import BytesIO
        import langdetect
    except ImportError:
        console.print("[bold red][CRITICAL][/bold red] pydub oder langdetect fehlt! → pip install pydub langdetect")
        return "FINISHED"

    async def generate_audio(text, voice, rate, pitch):
        try:
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return AudioSegment.from_file(BytesIO(audio_data), format="mp3")

        except Exception as edge_err:
            err_msg = str(edge_err)
            if "403" in err_msg or "response status" in err_msg.lower():
                console.print(f"[bold yellow][WARN][/bold yellow] Cloud-Blockade (403) bei {owner_key} erkannt. Schalte lokale SAPI ein...")
                
                speaker = win32com.client.Dispatch("SAPI.SpVoice")
                found_voice = False
                for v in speaker.GetVoices():
                    if "Katja" in v.GetDescription() or "Amala" in v.GetDescription() or "Stefan" in v.GetDescription():
                        speaker.Voice = v
                        found_voice = True
                        break
                
                if not found_voice:
                    for v in speaker.GetVoices():
                        if "Hedda" in v.GetDescription() or "German" in v.GetDescription():
                            speaker.Voice = v
                            break
                
                temp_sapi = os.path.join(CACHE_DIR, f"sapi_fallback_{owner_key}.wav")
                filestream = win32com.client.Dispatch("SAPI.SpFileStream")
                filestream.Open(temp_sapi, 3, False)
                speaker.AudioOutputStream = filestream
                speaker.Speak(text)
                filestream.Close()
                
                console.print(f"[bold green][SUCCESS][/bold green] Notfall-Audio über lokale SAPI generiert.")
                return AudioSegment.from_file(temp_sapi, format="wav")
            else:
                raise edge_err

    def split_into_segments(text):
        parts = re.split(r'(?<=[.!?])\s+|\n+', text.strip())
        english_starters = [
            "meanwhile", "the", "and", "this", "that", "however", "finally",
            "now", "here", "there", "when", "while", "although", "because",
            "across", "whether", "once", "after", "before", "during", "if",
            "but", "yet", "even", "only"
        ]

        segments = []
        current_lang = "de"

        for part in parts:
            part = part.strip()
            if not part:
                continue

            lower = part.lower()
            first_word = lower.split() if lower.split() else ""

            if first_word in english_starters:
                lang = "en"
            else:
                try:
                    detected = langdetect.detect(part)
                    lang = "en" if detected.startswith("en") else "de"
                except:
                    lang = current_lang

            english_indicators = ["the", "and", "of", "to", "in", "is", "that", "for", "it", "with", "as", "on", "at"]
            words = lower.split()
            if len(words) > 6:
                en_count = sum(1 for w in words if w in english_indicators)
                if en_count >= 4:
                    lang = "en"

            segments.append((lang, part))
            current_lang = lang

        return segments

    # =======================================================================
    # AUDIO IN SCHNELLEN CHUNKS ZUSAMMENBAUEN & ABSPIELEN
    # =======================================================================
    ffplay_path = os.path.join(BASE_DIR, "ffplay.exe")

    async def play_segment_audio(audio_seg, block_idx):
        if len(audio_seg) == 0:
            return "CONTINUE"
        temp_mp3 = os.path.abspath(os.path.join(CACHE_DIR, f"voice_{owner_key}_{block_idx}.mp3"))
        audio_seg.export(temp_mp3, format="mp3")

        cmd = [ffplay_path, "-nodisp", "-autoexit", "-hide_banner", "-loglevel", "error", temp_mp3]
        proc = subprocess.Popen(cmd, creationflags=0x08000000)
        start_time = time.time()

        while proc.poll() is None:
            if (time.time() - start_time) > 600:
                proc.terminate()
                break
            if os.path.exists(P_FILE):
                proc.terminate()
                return "PAUSED"
            if os.path.exists(N_FILE):
                proc.terminate()
                return "SKIPPED"
            await asyncio.sleep(0.2)

        try:
            if os.path.exists(temp_mp3): os.remove(temp_mp3)
        except: pass
        return "CONTINUE"

    if use_split:
        raw_segments = split_into_segments(full_text)
        text_chunks = []
        current_chunk = []
        current_len = 0

        for lang, seg_text in raw_segments:
            if not re.search(r'[a-zA-ZäöüÄÖÜß]', seg_text):
                continue
            current_chunk.append((lang, seg_text))
            current_len += len(seg_text)
            if current_len >= 1500:
                text_chunks.append(current_chunk)
                current_chunk = []
                current_len = 0
        if current_chunk:
            text_chunks.append(current_chunk)

        chunk_count = max(1, len(text_chunks))
        console.print(f"[bold {color}][{display_name}][/bold {color}] [grey]{uhrzeit}[/grey] ({chunk_count} Ch {CURRENT_RAM_COUNT} Z): \"{safe_preview}...\"")

        for c_idx, chunk_segments in enumerate(text_chunks):
            combined_chunk = AudioSegment.empty()
            for lang, seg_text in chunk_segments:
                voice, rate, pitch = (voice_de, rate_de, pitch_de) if lang.startswith("de") else (voice_en, rate_en, pitch_en)
                try:
                    combined_chunk += await generate_audio(seg_text, voice, rate, pitch)
                except Exception as e:
                    console.print(f"[bold yellow]Segment-Fehler ({lang}): {e}[/bold yellow]")
            
            play_status = await play_segment_audio(combined_chunk, c_idx)
            if play_status in ["PAUSED", "SKIPPED"]:
                return play_status
    else:
        console.print(f"[bold {color}][{display_name}][/bold {color}] [grey]{uhrzeit}[/grey] (1 Ch {CURRENT_RAM_COUNT} Z): \"{safe_preview}...\"")
        rate = ticket.get('rate', '+9%')
        pitch = ticket.get('pitch', '+2Hz')
        try:
            audio = await generate_audio(full_text, single_voice, rate, pitch)
            play_status = await play_segment_audio(audio, 0)
            if play_status in ["PAUSED", "SKIPPED"]:
                return play_status
        except Exception as e:
            console.print(f"[bold red]TTS-Fehler: {e}[/bold red]")

    return "FINISHED"


async def main_loop():
    global CURRENT_RAM_COUNT  
    console.print("[bold green][CHECK][/bold green] Titan-Butler v45.1 (Fast-Split-Engine) Online.")
    await asyncio.sleep(2) 

    cfg = {
        "voice_de": "de-DE-TanjaNeural",
        "rate_de": "+9%",
        "pitch_de": "+2Hz",
        "welcome_text": "System online. Ich höre dich, Architekt."
    }
    priv_path = os.path.join(BASE_DIR, "private_voice.json")
    if os.path.exists(priv_path):
        try:
            with open(priv_path, "r", encoding="utf-8") as f: cfg.update(json.load(f))
        except: pass

    await speak_and_wait({
        "text": cfg["welcome_text"],
        "owner": "GEE",
        "voice": cfg["voice_de"],
        "rate": cfg["rate_de"],
        "pitch": cfg["pitch_de"]
    })

    while True:
        file_path = "" 
        try:
            if os.path.exists(P_FILE):
                await asyncio.sleep(0.5); continue

            active = sorted([f for f in os.listdir(SAFE_DIR) if f.endswith(".json")])
            if not active:
                queue = sorted([f for f in os.listdir(Q_DIR) if f.endswith(".json")])
                if not queue:
                    await asyncio.sleep(0.5); continue
                
                source = os.path.join(Q_DIR, queue[0])
                file_path = os.path.join(SAFE_DIR, f"{int(time.time()*1000)}_{queue[0]}")
                shutil.move(source, file_path)
            else:
                file_path = os.path.join(SAFE_DIR, active[0])

            with open(file_path, "r", encoding="utf-8-sig") as j:
                ticket = json.load(j)

            owner_key = ticket.get('owner', 'UNKNOWN').upper()
            received_text = ticket.get('text', '').casefold()
            
            is_monkey_reset = "reset_signal" in received_text
            is_bat_reset = "spickzettel verbrannt" in received_text

            if is_monkey_reset or is_bat_reset:
                CURRENT_RAM_COUNT = 0  
                try:
                    with open(LIMIT_FILE, "w", encoding="utf-8") as f: f.write("0")
                except: pass
                
                console.print("[bold green][RESET][/bold green] Spickzettel verbrannt. RAM & Datei auf Null.")
                
                if os.path.exists(file_path):
                    try: os.remove(file_path)
                    except:
                        try: os.rename(file_path, file_path + ".dead")
                        except: pass
                continue  

            elif owner_key == "GEE":
                try:
                    if os.path.exists(LIMIT_FILE):
                        with open(LIMIT_FILE, "r", encoding="utf-8") as f:
                            data = f.read().strip()
                            CURRENT_RAM_COUNT = int(data) if data else 0
                    else:
                        CURRENT_RAM_COUNT = 0
                except: 
                    pass
                
                CURRENT_RAM_COUNT += len(ticket.get('text', '')) + 600
                
                try:
                    with open(LIMIT_FILE, "w", encoding="utf-8") as f: f.write(str(CURRENT_RAM_COUNT))
                except: pass

                if CURRENT_RAM_COUNT > 215000:
                    console.print("[bold white on red][ WARNUNG ][/bold white on red] KONTEXT-LIMIT ERREICHT!")
                    import winsound
                    winsound.Beep(1000, 500)  
                    
                    bat_path = os.path.abspath(os.path.join(BASE_DIR, "..", "S403_Clear_Counter.bat"))
                    if os.path.exists(bat_path):
                        subprocess.Popen([bat_path], shell=True, cwd=os.path.dirname(bat_path))
                        console.print("[bold green][AUTO-SYS][/bold green] S403_Clear_Counter.bat automatisch abgefeuert!")

            status = await speak_and_wait(ticket)

            if status == "PAUSED":
                continue  

            if status in ["FINISHED", "SKIPPED"]:
                await asyncio.sleep(0.5)
                if os.path.exists(file_path):
                    try: os.remove(file_path)
                    except Exception as e:
                        console.print(f"[Reinigung] Blockiert: {e}")
                        try:
                            os.rename(file_path, file_path + ".dead")
                        except: pass

                if status == "SKIPPED" and os.path.exists(N_FILE):
                    try: os.remove(N_FILE)
                    except: pass

        except Exception as e:
            console.print(f"[Loop-Fehler] {e}")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main_loop())

