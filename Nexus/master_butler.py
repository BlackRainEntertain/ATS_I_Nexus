import os, sys, json, time, asyncio, edge_tts, subprocess, re, shutil
from rich.console import Console

os.system("title AUDIO_MASTER_BUTLER")
console = Console()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Q_DIR = os.path.join(BASE_DIR, "_Voice_Queue")
SAFE_DIR = os.path.join(BASE_DIR, "_Active_Ticket") # DER TRESOR
P_FILE = os.path.join(BASE_DIR, "NEXUS_PAUSE.tmp")
N_FILE = os.path.join(BASE_DIR, "NEXUS_NEXT.tmp")

if not os.path.exists(SAFE_DIR): os.makedirs(SAFE_DIR)

async def speak_and_wait(ticket):
    text = re.sub(r'[={}_#<>]', ' ', ticket.get('text', ''))
    owner = ticket.get('owner', 'UNKNOWN').upper()
    temp_mp3 = os.path.abspath(os.path.join(BASE_DIR, f"voice_{owner}.mp3"))
    try:
        await edge_tts.Communicate(text, ticket.get('voice', 'de-DE-KatjaNeural'), rate="+15%").save(temp_mp3)
        console.print(f"[bold cyan][{owner}][/bold cyan] spricht: [dim]\"{text[:50]}...\"[/dim]")
        
        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_mp3}'); $p.Play(); Start-Sleep -s {int(len(text)/10+6)}; $p.Close()"
        proc = subprocess.Popen(["powershell", "-c", ps_cmd], creationflags=0x08000000)
        
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
    except: return "ERROR"

async def main_loop():
    if not os.path.exists(Q_DIR): os.makedirs(Q_DIR)
    console.print("[bold green][CHECK][/bold green] Titan-Butler v38.0 (Tresor-Schutz) Online.")
    # Begrüssung
    await speak_and_wait({"text": "System online. Ich höre dich, Architekt.", "owner": "GEE"})
    
    while True:
        try:
            if os.path.exists(P_FILE):
                await asyncio.sleep(0.5); continue

            # 1. Zuerst im Tresor nachsehen (Unterbrochene Nachrichten)
            active_files = [f for f in os.listdir(SAFE_DIR) if f.endswith(".json")]
            if active_files:
                file_path = os.path.join(SAFE_DIR, active_files[0])
            else:
                # 2. Wenn Tresor leer, nimm neues Ticket aus der Queue
                queue_files = sorted([f for f in os.listdir(Q_DIR) if f.endswith(".json")])
                if queue_files:
                    source = os.path.join(Q_DIR, queue_files[0])
                    file_path = os.path.join(SAFE_DIR, queue_files[0])
                    shutil.move(source, file_path) # VERSCHIEBEN STATT LÖSCHEN
                else:
                    await asyncio.sleep(0.5); continue

            with open(file_path, "r", encoding="utf-8-sig") as j:
                ticket = json.load(j)
            
            status = await speak_and_wait(ticket)
            
            # 3. LÖSCH-GARANTIE: Nur bei Erfolg oder manuellem Skip
            if status in ["FINISHED", "SKIPPED"]:
                if os.path.exists(file_path):
                    try: os.remove(file_path)
                    except: pass
            # Bei PAUSED bleibt das Ticket einfach im SAFE_DIR liegen!
            
        except Exception as e:
            console.print(f"[Loop-Fehler] {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main_loop())




