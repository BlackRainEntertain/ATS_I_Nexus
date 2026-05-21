import os, sys, json, time, asyncio, edge_tts, subprocess, re, shutil
from rich.console import Console
from rich.markup import escape
from datetime import datetime
CURRENT_RAM_COUNT = 0  # Globaler Zähler im schnellen Arbeitsspeicher

os.system("title AUDIO_MASTER_BUTLER_V43.9_TITAN_ULTRA")
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
    global CURRENT_RAM_COUNT  # HIER REIN! Jetzt zieht sich die Funktion den echten Live-Stand aus dem Hub.
    full_text = re.sub(r'[={}_#<>]', ' ', ticket.get('text', ''))
    
    # --- STUMMSCHALTUNG FÜR SYSTEM-SIGNALE ---
    if "RESET_SIGNAL" in full_text: 
        return "FINISHED"

    # 1. Routing-Key (für Farben & Logik)
    owner_key = ticket.get('owner', 'UNKNOWN').upper()
    
    # 2. Anzeige-Name (Die "Taufe")
    raw_sender = ticket.get('sender')
    display_name = (raw_sender if raw_sender else owner_key).upper()
    
    voice = ticket.get('voice', 'de-DE-KatjaNeural')
    chunks = [full_text[i:i+5000] for i in range(0, len(full_text), 5000)]
    
    # 3. Farben-Check bleibt auf dem Key (META), damit es bunt bleibt
    colors = {"GEE": "bright_blue", "NEXUS": "cyan", "META": "magenta", "ATSI": "bright_cyan", "GROK": "#FFEE00"}
    color = colors.get(owner_key, "white") # Nutzt META für die Farbe
    
    uhrzeit = datetime.now().strftime("%H:%M:%S")
    safe_preview = escape(full_text[:60].replace("\n", " "))
    
    # JETZT die ultrakompakte Cockpit-Anzeige am Heck eingeflochten! 
    console.print(f"[bold {color}][{display_name}][/bold {color}] [grey]{uhrzeit}[/grey] ({len(chunks)} Ch {CURRENT_RAM_COUNT} Z): \"{safe_preview}...\"")



    # --- REINIGUNG DER ZOMBIE-CHUNKS (v43.9-Mod) ---
    for f in os.listdir(CACHE_DIR):
        # WICHTIG: Nutze owner_key, damit er die META-Dateien findet
        if f.startswith(f"voice_{owner_key}_") and not f.endswith("_0.mp3") and f.endswith(".mp3"):
            try: os.remove(os.path.join(CACHE_DIR, f))
            except: pass

    for idx, chunk in enumerate(chunks):
        if not chunk.strip(): continue
        # WICHTIG: Auch hier owner_key nutzen für den physischen Dateinamen
        temp_mp3 = os.path.abspath(os.path.join(CACHE_DIR, f"voice_{owner_key}_{idx}.mp3"))
        
        try:
            # --- SPERRBRECHER ---
            if os.path.exists(temp_mp3):
                try:
                    with open(temp_mp3, 'a'): pass 
                except IOError:
                    subprocess.run("taskkill /f /t /im pwsh.exe", shell=True, capture_output=True)
                    subprocess.run("taskkill /f /t /im powershell.exe", shell=True, capture_output=True)
                    await asyncio.sleep(0.2)

            await edge_tts.Communicate(chunk, voice, rate="+15%").save(temp_mp3)
            
            # --- TITAN-BYPASS v44.8 (FFPLAY-DIRECT) ---
            ffplay_path = os.path.join(BASE_DIR, "ffplay.exe")
            
            # -nodisp = kein Fenster | -autoexit = schliesst sich selbst
            cmd = [
                ffplay_path, "-nodisp", "-autoexit", 
                "-hide_banner", "-loglevel", "error", temp_mp3
            ]
            
            # Startet den Player komplett im Hintergrund (kein Poppup)
            proc = subprocess.Popen(cmd, creationflags=0x08000000)
            
            # --- DER LUNGEN-PATCH (Vollständige Wiedergabe) ---
            start_time = time.time()
            # 600 Sekunden (10 Min) sind genug für jeden 5000-Zeichen-Chunk.
            max_safety_timeout = 600 

            while proc.poll() is None:
                # 1. Nur noch Notfall-Sicherung gegen echte Freezes
                if (time.time() - start_time) > max_safety_timeout:
                    console.print("[bold red][TIMEOUT][/bold red] Sicherheitsstopp (10min überschritten).")
                    proc.terminate()
                    break
                
                # 2. Pause-Check (Ticket bleibt im Safe-Ordner)
                if os.path.exists(P_FILE): 
                    proc.terminate()
                    return "PAUSED"
                
                # 3. Skip-Check (Bricht aktuellen Chunk/Ticket ab)
                if os.path.exists(N_FILE):
                    proc.terminate()
                    return "SKIPPED"
                
                await asyncio.sleep(0.3) # Entlastet die CPU während der Wiedergabe


            # Reinigung der temporären Chunks nach dem Abspielen
            if idx > 0 and os.path.exists(temp_mp3):
                try: os.remove(temp_mp3)
                except: pass

        except Exception as e:
            console.print(f"[bold yellow][WARN][/bold yellow] Chunk {idx} fehlgeschlagen: {e}")
            continue
    return "FINISHED"


async def main_loop():
    global CURRENT_RAM_COUNT  # Einmalig ganz oben deklariert für die ganze Funktion
    console.print("[bold green][CHECK][/bold green] Titan-Butler v44.0 (Ultra: Context-Guard) Online.")
    await asyncio.sleep(2) 
    await speak_and_wait({"text": "System online. Ich höre dich, Architekt.", "owner": "GEE"})

    while True:
        file_path = "" 
        try:
            # 1. PAUSE-CHECK
            if os.path.exists(P_FILE):
                await asyncio.sleep(0.5); continue

            # 2. TICKET-ACQUISITION (Safe-First Logik)
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
            
            # 1. DER RADIKALE RESET-CHECK (Rückstandsfreie Hub-Sicherung v46.1)
            is_monkey_reset = "reset_signal" in received_text
            is_bat_reset = "spickzettel verbrannt" in received_text

            if is_monkey_reset or is_bat_reset:
                CURRENT_RAM_COUNT = 0  # RAM-Zähler auf Null
                
                try:
                    with open(LIMIT_FILE, "w", encoding="utf-8") as f: f.write("0")
                except: pass
                
                console.print("[bold green][RESET][/bold green] Spickzettel verbrannt. RAM & Datei auf Null.")
                
                # ABSOLUTE REINIGUNG DES INFO-TICKETS
                if os.path.exists(file_path):
                    try: os.remove(file_path)
                    except:
                        try: os.rename(file_path, file_path + ".dead")
                        except: pass
                        
                continue  # Schleife springt sicher und rückstandslos zum nächsten Hub-Ticket!

            # 2. DER REIN SYNCHRONISIERTE GEE-CHECK (Mit vollautomatischer .bat-Zündung!)
            elif owner_key == "GEE":
                # Das physische Gedächtnis: Der Butler zieht die Zahl bei JEDEM Ticket direkt aus der Datei
                try:
                    if os.path.exists(LIMIT_FILE):
                        with open(LIMIT_FILE, "r", encoding="utf-8") as f:
                            data = f.read().strip()
                            CURRENT_RAM_COUNT = int(data) if data else 0
                    else:
                        CURRENT_RAM_COUNT = 0
                except: 
                    pass
                
                # Reguläre Berechnung basierend auf dem geladenen Dateistand
                CURRENT_RAM_COUNT += len(ticket.get('text', '')) + 600
                
                # Schreibt den neuen Wert sofort wieder zurück auf die Festplatte
                try:
                    with open(LIMIT_FILE, "w", encoding="utf-8") as f: f.write(str(CURRENT_RAM_COUNT))
                except: pass

                # DIE RETTUNGS-ZÜNDUNG (Deine .bat wird bei 215k automatisch gefeuert)
                if CURRENT_RAM_COUNT > 215000:
                    console.print("[bold white on red][ WARNUNG ][/bold white on red] KONTEXT-LIMIT ERREICHT!")
                    import winsound
                    winsound.Beep(1000, 500)  # Dein Warn-Piepen auf dem Ohr!
                    
                    bat_path = os.path.abspath(os.path.join(BASE_DIR, "..", "S403_Clear_Counter.bat"))
                    if os.path.exists(bat_path):
                        subprocess.Popen([bat_path], shell=True, cwd=os.path.dirname(bat_path))
                        console.print("[bold green][AUTO-SYS][/bold green] S403_Clear_Counter.bat automatisch abgefeuert!")

            # 3. SPRACHAUSGABE STARTEN
            status = await speak_and_wait(ticket)

            if status == "PAUSED":
                continue  

            # 4. REINIGUNG NACH ABSCHLUSS
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

