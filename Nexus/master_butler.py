import os, sys, json, time, asyncio, edge_tts, subprocess, re, shutil
from rich.console import Console

os.system("title AUDIO_MASTER_BUTLER")
console = Console()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Q_DIR = os.path.join(BASE_DIR, "_Voice_Queue")
SAFE_DIR = os.path.join(BASE_DIR, "_Active_Ticket")
P_FILE = os.path.join(BASE_DIR, "NEXUS_PAUSE.tmp")
N_FILE = os.path.join(BASE_DIR, "NEXUS_NEXT.tmp")

if not os.path.exists(SAFE_DIR): os.makedirs(SAFE_DIR)

async def speak_and_wait(ticket):
    text = re.sub(r'[={}_#<>]', ' ', ticket.get('text', ''))
    owner = ticket.get('owner', 'UNKNOWN').upper()
    temp_mp3 = os.path.abspath(os.path.join(BASE_DIR, f"voice_{owner}.mp3"))
    ps_p_file, ps_n_file = P_FILE, N_FILE
    uri_path = "file:///" + temp_mp3.replace("\\", "/").replace(" ", "%20")
    try:
        await edge_tts.Communicate(text, ticket.get('voice', 'de-DE-KatjaNeural'), rate="+15%").save(temp_mp3)
        console.print(f"[bold cyan][{owner}][/bold cyan] spricht: [dim]\"{text[:50]}...\"[/dim]")
        ps_script = f"""
        Add-Type -AssemblyName PresentationCore
        $p = New-Object System.Windows.Media.MediaPlayer; $p.Open("{uri_path}")
        $w = 0; while ($p.NaturalDuration.HasTimeSpan -eq $false -and $w -lt 50) {{ Start-Sleep -ms 100; $w++ }}
        $p.Play(); $s = Get-Date
        while ($p.Position -lt $p.NaturalDuration.TimeSpan -and (Get-Date) -lt $s.AddSeconds(120)) {{
            if (Test-Path "{ps_p_file}" -or Test-Path "{ps_n_file}") {{ $p.Stop(); $p.Close(); exit }}
            Start-Sleep -ms 200
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
    if not os.path.exists(Q_DIR): os.makedirs(Q_DIR)
    console.print("[bold green][CHECK][/bold green] Titan-Butler v38.0 (Tresor-Schutz) Online.")
    await speak_and_wait({"text": "System online. Ich höre dich, Architekt.", "owner": "GEE"})
    
    while True:
        try:
            if os.path.exists(P_FILE):
                await asyncio.sleep(0.5); continue

            active_files = sorted([f for f in os.listdir(SAFE_DIR) if f.endswith(".json")])
            
            if active_files:
                file_path = os.path.join(SAFE_DIR, active_files[0]) # INDEX FIX
            else:
                queue_files = sorted([f for f in os.listdir(Q_DIR) if f.endswith(".json")])
                if queue_files:
                    source_name = queue_files[0] # VARIABLE FIX
                    source_path = os.path.join(Q_DIR, source_name)
                    unique_name = f"{int(time.time() * 1000)}_{source_name}"
                    file_path = os.path.join(SAFE_DIR, unique_name)
                    
                    shutil.move(source_path, file_path) 
                else:
                    await asyncio.sleep(0.5); continue

            with open(file_path, "r", encoding="utf-8-sig") as j:
                ticket = json.load(j)
            
            status = await speak_and_wait(ticket)
            
            if status in ["FINISHED", "SKIPPED"]:
                if os.path.exists(file_path):
                    os.remove(file_path)
            
        except Exception as e:
            console.print(f"[Loop-Fehler] {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main_loop())







