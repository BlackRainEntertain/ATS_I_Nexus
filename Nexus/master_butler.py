import os, sys, json, time, asyncio, edge_tts, subprocess, re, shutil
from rich.console import Console
from rich.markup import escape

os.system("title AUDIO_MASTER_BUTLER")
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
    text = re.sub(r'[={}_#<>]', ' ', ticket.get('text', ''))
    owner = ticket.get('owner', 'UNKNOWN').upper()
    voice = ticket.get('voice', 'de-DE-KatjaNeural')
    temp_mp3 = os.path.abspath(os.path.join(BASE_DIR, f"voice_{owner}.mp3"))
    uri_path = "file:///" + temp_mp3.replace("\\", "/").replace(" ", "%20")
    
    try:
        await edge_tts.Communicate(text, voice, rate="+15%").save(temp_mp3)
        
        # UI-Feedback (v43.1 mit Uhrzeit-Stempel)
        from datetime import datetime
        uhrzeit = datetime.now().strftime("%H:%M:%S")
        
        colors = {"GEE": "bright_blue", "NEXUS": "cyan", "META": "magenta", "ATSI": "bright_cyan"}
        color = colors.get(owner, "white")
        safe_text = escape(text[:60].replace("\n", " "))
        
        # Der neue Look: [OWNER] Uhrzeit spricht: "Text..."
        console.print(f"[bold {color}][{owner}][/bold {color}] [grey]{uhrzeit}[/grey] spricht: \"{safe_text}...\"")


        # Audio-Vektor (PowerShell Mediaplayer)
        max_sec = max(5, int(len(text.split()) * 0.7) + 5)
        ps_script = f"""
        Add-Type -AssemblyName PresentationCore
        $p = New-Object System.Windows.Media.MediaPlayer
        $p.Open('{uri_path.replace("'", "''")}')
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
                if os.path.exists(N_FILE): os.remove(N_FILE)
                return "SKIPPED"
            await asyncio.sleep(0.2)
        return "FINISHED"
    except Exception as e:
        console.print(f"[ERR] {e}"); return "ERROR"

async def main_loop():
    warned_217k = False
    console.print("[bold green][CHECK][/bold green] Titan-Butler v42.8 Online.")
    
    # --- DER 2-SEKUNDEN-PUFFER BEIM START ---
    await asyncio.sleep(2) 

    # --- JETZT ERST DIE BEGRÜSSUNG ---
    await speak_and_wait({"text": "System online. Ich höre dich, Architekt.", "owner": "GEE"})


    while True:
        try:
            if os.path.exists(P_FILE):
                await asyncio.sleep(0.5); continue

            # Queue-Handling
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

            # --- SESSION CONTEXT LOGIK ---
            if ticket.get('owner') == "GEE":
                try:
                    count = int(open(LIMIT_FILE, "r").read()) if os.path.exists(LIMIT_FILE) else 0
                except: count = 0
                
                if "Erforschung nicht-linearer Interferenzmuster" in ticket.get('text', ''):
                    count = 0
                else:
                    count += len(ticket.get('text', '')) + 600
                
                with open(LIMIT_FILE, "w") as f: f.write(str(count))
                
                if count >= 217000 and not warned_217k:
                    await speak_and_wait({"text": "Achtung. Kontext-Sättigung erreicht.", "owner": "NEXUS"})
                    warned_217k = True
                elif count < 217000: warned_217k = False

            # 1. Audio-Ausgabe triggern
            status = await speak_and_wait(ticket)
            
            # 2. SIGNAL-REINIGUNG & WARTESCHLEIFE
            if status == "SKIPPED":
                # Gib dem System Zeit, den Skip-Kill physisch zu verdauen
                await asyncio.sleep(0.6) 
                if os.path.exists(N_FILE):
                    try: os.remove(N_FILE)
                    except: pass
            
            # 3. TICKET-SCHUTZ: Nur löschen, wenn wirklich beendet
            if status in ["FINISHED", "SKIPPED"]:
                # Prüfe kurz, ob die MP3 noch vom System gesperrt ist
                await asyncio.sleep(0.2) 
                if os.path.exists(file_path): 
                    try: os.remove(file_path)
                    except: pass # Falls Datei noch offen, nächsten Loop abwarten


        except Exception as e:
            console.print(f"[Loop-Fehler] {e}"); await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main_loop())

