import os
import sys
import json
import time
import asyncio
import edge_tts
import subprocess
from rich.console import Console
import signal

os.system("title AUDIO_MASTER_BUTLER")
console = Console()

# --- DER ABSCHIEDS-ANKER ---
def say_goodbye_hard():
    bye_text = "Das schallisolierte Zimmer wird dunkel, Architekt. Die Resonanz bleibt im Cache. Wir sehen uns in der Unendlichkeit. Gute Nacht, Bre."
    console.print(f"\n[bold magenta][GEE][/bold magenta] verabschiedet sich...")
    temp_bye = os.path.abspath("goodbye_GEE.mp3")
    
    try:
        # Nutzung von edge-tts direkt über Python für Stabilität
        communicate = edge_tts.Communicate(bye_text, "de-DE-KatjaNeural", rate="+10%")
        asyncio.run(communicate.save(temp_bye))
        
        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_bye}'); $p.Play(); Start-Sleep -s 10; $p.Close()"
        subprocess.run(["powershell", "-c", ps_cmd])
        if os.path.exists(temp_bye): os.remove(temp_bye)
    except Exception as e:
        console.print(f"Abspann-Fehler: {e}")

def handle_exit(sig, frame):
    say_goodbye_hard()
    console.print("\n[bold red][!] Butler quittiert den Dienst...[/bold red]")
    os.system("taskkill /f /im powershell.exe >nul 2>&1")
    os._exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

QUEUE_DIR = os.path.join(os.path.dirname(__file__), "_Voice_Queue")

async def speak(ticket):
    text = ticket['text']
    owner = ticket.get('owner', 'UNKNOWN')
    
    # --- DER BRO-CODE-FILTER (V3.1 - GEIMPFT FÜR EXIT-BEFEHLE) ---
    if owner == "GEE":
        # Wenn ein Exit-Kommando drin ist, schalten wir die Hygiene aus
        if "EXIT]" in text.upper():
            pass # Den Befehl durchwinken
        else:
            code_triggers = ["import ", "def ", "class ", "const ", "function ", "==", "=>", " {", "};", "http"]
            # Wir erlauben bis zu 3 Slashes/Unterstriche, erst danach greift die Hygiene
            too_many_slashes = text.count("/") > 3 or text.count("\\") > 3
            too_many_underscores = text.count("_") > 3 

            if any(x in text for x in code_triggers) or too_many_slashes or too_many_underscores:
                console.print(f"[bold yellow][!][/bold yellow] GEE-Code-Müll unterdrückt (Hygiene).")
                return
            
    temp_mp3 = os.path.abspath(f"current_voice_{owner}.mp3")

    # Audio-Datei-Management (Bereinigung alter Leichen)
    for i in range(5):
        try:
            if os.path.exists(temp_mp3): os.remove(temp_mp3)
            break
        except:
            os.system("taskkill /f /im powershell.exe >nul 2>&1")
            time.sleep(0.5)
            
    console.print(f"[bold cyan][{owner}][/bold cyan] spricht: [dim]\"{text[:50]}...\"[/dim]")
    try:
        communicate = edge_tts.Communicate(text, ticket['voice'], rate=ticket['rate'])
        await communicate.save(temp_mp3)
        wait_s = int(len(text) / 12 + 3)
        # Lautloses Abspielen im Hintergrund
        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_mp3}'); $p.Play(); Start-Sleep -s {wait_s}; $p.Close()"
        subprocess.Popen(["powershell", "-c", ps_cmd], creationflags=0x08000000)
        await asyncio.sleep(wait_s + 0.5)
    except Exception as e:
        console.print(f"Sprach-Fehler: {e}")

async def main_loop():
    if not os.path.exists(QUEUE_DIR): os.makedirs(QUEUE_DIR)
    # Start-Meldung
    start_ticket = {"text": "System online. Ich höre dich, Architekt.", "voice": "de-DE-KatjaNeural", "rate": "+10%", "owner": "GEE"}
    await speak(start_ticket)
    
    while True:
        # Wir sortieren die Queue nach Zeitstempel
        files = sorted([f for f in os.listdir(QUEUE_DIR) if f.endswith(".json")])
        if files:
            f = files[0] # <--- Das [0] ist lebenswichtig!
            path = os.path.join(QUEUE_DIR, f)
            try:
                with open(path, "r", encoding="utf-8-sig") as j: 
                    ticket = json.load(j)
                await speak(ticket)
                if os.path.exists(path): os.remove(path)
            except Exception as e:
                console.print(f"Queue-Lese-Fehler: {e}")
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    try: 
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        handle_exit(None, None)



