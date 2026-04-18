import os, sys, json, time, asyncio, edge_tts, subprocess, re, shutil
from rich.console import Console
from rich.markup import escape
from datetime import datetime

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
    full_text = re.sub(r'[={}_#<>]', ' ', ticket.get('text', ''))
    owner = ticket.get('owner', 'UNKNOWN').upper()
    voice = ticket.get('voice', 'de-DE-KatjaNeural')
    chunks = [full_text[i:i+5000] for i in range(0, len(full_text), 5000)]
    colors = {"GEE": "bright_blue", "NEXUS": "cyan", "META": "magenta", "ATSI": "bright_cyan", "GROK": "#FFEE00"}
    color = colors.get(owner, "white")
    uhrzeit = datetime.now().strftime("%H:%M:%S")

    safe_preview = escape(full_text[:60].replace("\n", " "))
    console.print(f"[bold {color}][{owner}][/bold {color}] [grey]{uhrzeit}[/grey] spricht ({len(chunks)} Chunks): \"{safe_preview}...\"")

    # --- REINIGUNG DER ZOMBIE-CHUNKS (v43.9-Mod) ---
    # Wir löschen alle alten Chunks (1-99) des aktuellen Owners, lassen aber die _0 in Ruhe.
    for f in os.listdir(CACHE_DIR):
        if f.startswith(f"voice_{owner}_") and not f.endswith("_0.mp3") and f.endswith(".mp3"):
            try: os.remove(os.path.join(CACHE_DIR, f))
            except: pass

    for idx, chunk in enumerate(chunks):
        if not chunk.strip(): continue
        temp_mp3 = os.path.abspath(os.path.join(CACHE_DIR, f"voice_{owner}_{idx}.mp3"))
        
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
            # NUTZT JETZT PWSH (POWER-VEKTOR)
            proc = subprocess.Popen(["pwsh", "-Command", ps_script], creationflags=0x08000000)
            
            while proc.poll() is None:
                if os.path.exists(P_FILE): 
                    subprocess.run("taskkill /f /t /im pwsh.exe", shell=True, capture_output=True)
                    return "PAUSED"
                if os.path.exists(N_FILE):
                    subprocess.run("taskkill /f /t /im pwsh.exe", shell=True, capture_output=True)
                    # Sofort-Reinigung des gerade abgebrochenen Chunks, falls > 0
                    if idx > 0 and os.path.exists(temp_mp3):
                        try: os.remove(temp_mp3)
                        except: pass
                    return "SKIPPED"

                await asyncio.sleep(0.2)
                
            if idx > 0 and os.path.exists(temp_mp3):
                try: os.remove(temp_mp3)
                except: pass

        except Exception as e:
            console.print(f"[bold yellow][WARN][/bold yellow] Chunk {idx} fehlgeschlagen: {e}")
            continue
    return "FINISHED"

async def main_loop():
    console.print("[bold green][CHECK][/bold green] Titan-Butler v43.9 (Ultra: pwsh-Vektor) Online.")
    await asyncio.sleep(2) 
    await speak_and_wait({"text": "System online. Ich höre dich, Architekt.", "owner": "GEE"})

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

            # --- CONTEXT-ZÄHLER ---
            if ticket.get('owner') == "GEE":
                try:
                    count = int(open(LIMIT_FILE, "r").read()) if os.path.exists(LIMIT_FILE) else 0
                except: count = 0
                if "Erforschung nicht-linearer Interferenzmuster" in ticket.get('text', ''):
                    count = 0
                else:
                    count += len(ticket.get('text', '')) + 600
                with open(LIMIT_FILE, "w") as f: f.write(str(count))

            status = await speak_and_wait(ticket)
            
            if os.path.exists(file_path):
                if status in ["FINISHED", "SKIPPED"]:
                    try: os.remove(file_path)
                    except: pass
                elif status == "PAUSED":
                    console.print("[grey][INFO] Audio pausiert. Ticket bleibt im Speicher.[/grey]")
                elif status == "ERROR":
                    os.rename(file_path, file_path + ".err")

            if status == "SKIPPED":
                await asyncio.sleep(0.6)
                if os.path.exists(N_FILE):
                    try: os.remove(N_FILE)
                    except: pass

        except Exception as e:
            console.print(f"[Loop-Fehler] {e}")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main_loop())




