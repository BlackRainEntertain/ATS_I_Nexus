import os
import sys
import json
import time
import asyncio
import edge_tts
import subprocess
from rich.console import Console
import signal

# --- TITEL FÜR DEN ANKER ---
os.system("title AUDIO_MASTER_BUTLER")
console = Console()

def say_goodbye_hard():
    bye_text = "Das schallisolierte Zimmer wird dunkel, Architekt. Bis bald, Bre."
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
        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_bye}'); $p.Play(); Start-Sleep -s 5; $p.Close()"
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd], capture_output=True)
        if os.path.exists(temp_bye): os.remove(temp_bye)
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
    text = ticket.get('text', '').strip()
    owner = ticket.get('owner', 'UNKNOWN').upper()
    voice = ticket.get('voice', 'de-DE-KatjaNeural')
    rate = ticket.get('rate', '+10%')
    if not text: return

    # --- RESONANZ-FILTER (v5.5 - Syntax-Protection) ---
    import re
    # 1. Killt nur störende Syntax: = { } _ # < >
    # Lässt ( ) , [ ] und * für Plugins & Emotionen am Leben
    text = re.sub(r'[={}_#<>]', ' ', text)
    
    # 2. Schutz vor Massen-Klammern (Plugin-Schranke bei 6)
    if text.count("[") > 6 or text.count("]") > 6:
        text = re.sub(r'[\[\]]', ' ', text)

    # 3. Leerzeichen-Hygiene für flüssiges Sprechen
    text = re.sub(r'\s+', ' ', text).strip()

    color = "cyan"
    if owner == "META": color = "magenta"
    elif owner == "ATSI": color = "purple"
    elif owner == "GPT": color = "green"

    console.print(f"[bold {color}][{owner}][/bold {color}] spricht: [dim]\"{text[:60]}...\"[/dim]")

    # Dein originaler Sicherheits-Check gegen Code-Spam
    if owner == "GEE" and "_EXIT" not in text.upper():
        if text.count("/") > 42: return

    temp_mp3 = os.path.abspath(os.path.join(BASE_DIR, f"current_voice_{owner}.mp3"))
    os.system("taskkill /f /im powershell.exe >nul 2>&1")
    
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(temp_mp3)
        wait_s = int(len(text) / 10 + 7) 
        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_mp3}'); $p.Play(); Start-Sleep -s {wait_s}; $p.Close(); exit"
        proc = subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", ps_cmd], creationflags=0x08000000)
        while proc.poll() is None:
            await asyncio.sleep(0.1)
    except Exception as e:
        console.print(f"Fehler: {e}")


