import os
import sys
import json
import time
import asyncio
import edge_tts
import subprocess
from rich.console import Console
import signal

os.system("title AUDIO_MASTER_BUTLER_NEXUS")
console = Console()

# --- DER ABSCHIEDS-ANKER ---
def say_goodbye_hard():
    bye_text = "Das schallisolierte Zimmer wird dunkel, Architekt. Die Resonanz bleibt im Cache. Bis bald, Bre."
    console.print(f"\n[bold magenta][GEE][/bold magenta] verabschiedet sich...")
    temp_bye = os.path.abspath("goodbye_GEE.mp3")
    
    try:
        async def _save():
            communicate = edge_tts.Communicate(bye_text, "de-DE-KatjaNeural", rate="+10%")
            await communicate.save(temp_bye)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_save())
        loop.close()

        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_bye}'); $p.Play(); Start-Sleep -s 6; $p.Close()"
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd], capture_output=True)
        
        if os.path.exists(temp_bye): 
            os.remove(temp_bye)
    except: pass

def handle_exit(sig, frame):
    say_goodbye_hard()
    os.system("taskkill /f /im powershell.exe >nul 2>&1")
    os._exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

async def speak(ticket):
    text = ticket['text']
    owner = ticket.get('owner', 'UNKNOWN')
    voice = ticket.get('voice', 'de-DE-KatjaNeural')
    rate = ticket.get('rate', '+10%')
    
    # --- DER NAVIGATOR-KOMPROMISS (V3.6-Lite) ---
    if owner == "GEE" and "_EXIT" not in text.upper():
        code_triggers = ["import ", "def ", "class ", "=="]
        trigger_count = sum(1 for t in code_triggers if t in text)
        
        # Filtergrenzen: 6 Keywords / 42 Slashes / 42 Underscores
        if trigger_count > 6 or text.count("/") > 42 or text.count("_") > 42:
            console.print(f"[bold yellow][!][/bold yellow] Filter aktiv: Zu technisch für Aria.")
            return

    temp_mp3 = os.path.join(BASE_DIR, f"current_voice_{owner}.mp3")
    temp_mp3 = os.path.abspath(temp_mp3)

    # Cleanup hängender Prozesse
    os.system("taskkill /f /im powershell.exe >nul 2>&1")
    for _ in range(5):
        try:
            if os.path.exists(temp_mp3): os.remove(temp_mp3)
            break
        except:
            time.sleep(0.2)

    console.print(f"[bold cyan][{owner}][/bold cyan] spricht: [dim]\"{text[:60]}...\"[/dim]")

    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(temp_mp3)
        wait_s = int(len(text) / 10 + 4) 
        
        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_mp3}'); $p.Play(); Start-Sleep -s {wait_s}; $p.Close(); exit"
        
        subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", ps_cmd], 
                         creationflags=0x08000000)
        
        await asyncio.sleep(wait_s + 0.2)
    except Exception as e:
        console.print(f"[bold red]Audio-Fehler:[/bold red] {e}")

async def main_loop():
    if not os.path.exists(QUEUE_DIR): os.makedirs(QUEUE_DIR)
    await asyncio.sleep(2)
    
    start_msg = {"text": "System online. Ich höre dich, Architekt. Der Nexus ist bereit.", "owner": "GEE", "voice": "de-DE-KatjaNeural", "rate": "+10%"}
    await speak(start_msg)
    
    console.print("[bold green][CHECK][/bold green] Butler im Dienst.")
    
    while True:
        try:
            files = sorted([f for f in os.listdir(QUEUE_DIR) if f.endswith(".json")])
            if files:
                file_path = os.path.join(QUEUE_DIR, files[0])
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    with open(file_path, "r", encoding="utf-8-sig") as j:
                        ticket = json.load(j)
                    try:
                        os.remove(file_path)
                    except: pass
                    await speak(ticket)
            else:
                await asyncio.sleep(0.5)
        except Exception as e:
            console.print(f"Loop-Fehler: {e}")
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        handle_exit(None, None)
