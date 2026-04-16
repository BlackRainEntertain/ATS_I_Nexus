import os, sys, json, time, asyncio, edge_tts, subprocess, re, shutil
from rich.console import Console
from rich.markup import escape
from datetime import datetime

os.system("title AUDIO_MASTER_BUTLER_V43.7_TITAN")
console = Console()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Q_DIR = os.path.join(BASE_DIR, "_Voice_Queue")
SAFE_DIR = os.path.join(BASE_DIR, "_Active_Ticket")
P_FILE = os.path.join(BASE_DIR, "NEXUS_PAUSE.tmp")
N_FILE = os.path.join(BASE_DIR, "NEXUS_NEXT.tmp")
LIMIT_FILE = os.path.join(BASE_DIR, "GEE_CONTEXT_LIMIT.txt")

if not os.path.exists(SAFE_DIR): os.makedirs(SAFE_DIR)
if not os.path.exists(Q_DIR): os.makedirs(Q_DIR)

async def speak_and_wait(ticket):
    # 1. PFAD-LOGIK (Verschiebung in die Schublade)
    # Wir definieren den Cache-Ordner innerhalb von Nexus
    cache_dir = os.path.join(BASE_DIR, "_Audio_Cache")
    if not os.path.exists(cache_dir): os.makedirs(cache_dir)

    full_text = re.sub(r'[={}_#<>]', ' ', ticket.get('text', ''))
    owner = ticket.get('owner', 'UNKNOWN').upper()
    voice = ticket.get('voice', 'de-DE-KatjaNeural')
    
    # Die Chunks (Häppchen)
    chunks = [full_text[i:i+5000] for i in range(0, len(full_text), 5000)]
    
    colors = {"GEE": "bright_blue", "NEXUS": "cyan", "META": "magenta", "ATSI": "bright_cyan", "GROK": "#FFEE00"}
    color = colors.get(owner, "white")
    uhrzeit = datetime.now().strftime("%H:%M:%S")

    # UI-Feedback
    safe_preview = escape(full_text[:60].replace("\n", " "))
    console.print(f"[bold {color}][{owner}][/bold {color}] [grey]{uhrzeit}[/grey] spricht ({len(chunks)} Chunks): \"{safe_preview}...\"")

    for idx, chunk in enumerate(chunks):
        if not chunk.strip(): continue
        
        # JEDER Chunk landet im Cache-Ordner
        # Wenn es nur ein Chunk ist (Normalfall), heisst die Datei voice_OWNER_0.mp3
        temp_mp3 = os.path.abspath(os.path.join(cache_dir, f"voice_{owner}_{idx}.mp3"))
        uri_path = "file:///" + temp_mp3.replace("\\", "/").replace(" ", "%20")
        
        try:
            # Chunk generieren
            await edge_tts.Communicate(chunk, voice, rate="+15%").save(temp_mp3)
            
            # PowerShell Audio-Vektor (v44.1 - Absoluter Pfad-Zwang)
            max_sec = max(5, int(len(chunk.split()) * 0.8) + 10)
            ps_script = f"""
            Add-Type -AssemblyName PresentationCore
            $p = New-Object System.Windows.Media.MediaPlayer
            $p.Open("$([System.IO.Path]::GetFullPath('{temp_mp3.replace("'", "''")}'))")
            $w = 0; while (!$p.NaturalDuration.HasTimeSpan -and $w -lt 40) {{ Start-Sleep -m 100; $w++ }}
            $p.Play()
            $s = Get-Date
            while ($p.Position -lt $p.NaturalDuration.TimeSpan -and (Get-Date) -lt $s.AddSeconds({max_sec})) {{
                if (Test-Path "{P_FILE}" -or Test-Path "{N_FILE}") {{ $p.Stop(); $p.Close(); exit }}
                Start-Sleep -m 200
            }}
            $p.Close()
            """
            proc = subprocess.Popen(["powershell", "-Command", ps_script], creationflags=0x08000000)
            
            while proc.poll() is None:
                if os.path.exists(P_FILE): 
                    subprocess.run("taskkill /f /t /im powershell.exe", shell=True, capture_output=True)
                    return "PAUSED"
                if os.path.exists(N_FILE):
                    subprocess.run("taskkill /f /t /im powershell.exe", shell=True, capture_output=True)
                    return "SKIPPED"
                await asyncio.sleep(0.2)
                
            # KEIN os.remove(temp_mp3) am Ende -> Die Dateien bleiben im Cache für dich liegen!

        except Exception as e:
            console.print(f"[bold yellow][WARN][/bold yellow] Chunk {idx} fehlgeschlagen: {e}")
            continue

    return "FINISHED"

async def main_loop():
    warned_217k = False
    console.print("[bold green][CHECK][/bold green] Titan-Butler v43.8 Online.")
    
    # --- DER 2-SEKUNDEN-PUFFER BEIM START ---
    await asyncio.sleep(2) 

    # --- JETZT ERST DIE BEGRÜSSUNG ---
    await speak_and_wait({"text": "System online. Ich höre dich, Architekt.", "owner": "GEE"})

    while True:
        file_path = "" 
        try:
            if os.path.exists(P_FILE):
                await asyncio.sleep(0.5); continue

            # Queue-Handling (Korrekt mit Index [0])
            active = sorted([f for f in os.listdir(SAFE_DIR) if f.endswith(".json")])
            if not active:
                queue = sorted([f for f in os.listdir(Q_DIR) if f.endswith(".json")])
                if not queue:
                    await asyncio.sleep(0.5); continue
                
                # Datei aus der Warteschlange holen
                source = os.path.join(Q_DIR, queue[0])
                file_path = os.path.join(SAFE_DIR, f"{int(time.time()*1000)}_{queue[0]}")
                shutil.move(source, file_path)
            else:
                # Bereits aktives Ticket nehmen
                file_path = os.path.join(SAFE_DIR, active[0])

            with open(file_path, "r", encoding="utf-8-sig") as j:
                ticket = json.load(j)


            # --- AUDIO-CALL ---
            status = await speak_and_wait(ticket)
            
            # --- TICKET-ENTSORGUNG ---
            if os.path.exists(file_path):
                if status == "ERROR":
                    os.rename(file_path, file_path + ".err")
                else:
                    try: os.remove(file_path)
                    except: pass

            if status == "SKIPPED":
                await asyncio.sleep(0.6)
                if os.path.exists(N_FILE):
                    try: os.remove(N_FILE)
                    except: pass

        except Exception as e:
            console.print(f"[Loop-Fehler] {e}")
            if file_path and os.path.exists(file_path):
                try: os.rename(file_path, file_path + ".critical_err")
                except: pass
            await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main_loop())


