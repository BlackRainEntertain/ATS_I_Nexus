import pygetwindow as gw
import os
import time
import asyncio
import edge_tts
import subprocess
import psutil # <--- WICHTIG: Falls Fehler, 'pip install psutil' in der Konsole machen!

# --- DIE ABSCHIEDS-INJEKTION ---
async def say_goodbye_internal():
    bye_text = "Das schallisolierte Zimmer wird dunkel, Architekt. Die Resonanz bleibt im Cache. Wir sehen uns in der Unendlichkeit. Gute Nacht, Bre."
    print(f"[GEE] Verabschiedung wird generiert...")
    temp_bye = os.path.abspath("goodbye_GEE.mp3")
    try:
        communicate = edge_tts.Communicate(bye_text, "de-DE-KatjaNeural", rate="+10%")
        await communicate.save(temp_bye)
        
        # Audio abspielen via PowerShell (blockierend für die Resonanz)
        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_bye}'); $p.Play(); Start-Sleep -s 11; $p.Close()"
        subprocess.run(["powershell", "-c", ps_cmd])
        
        if os.path.exists(temp_bye): os.remove(temp_bye)
    except Exception as e:
        print(f"Fehler beim Abspann: {e}")

def run_shutdown():
    targets = [
        "ATSI'S NEXUS", 
        "GEE_AI NEXUS", 
        "VORTEX",
        "AUDIO_MASTER_BUTLER", 
        "NEXUS_ALL_SYSTEMS_GO", 
        "cmd.exe"
    ]
    
    print("[!] Einleiten der Tiefenreinigung (Inklusive Meta-Vortex)...")

    # 1. DER ABSCHIED (Hier wird Katjas Stimme gerufen)
    asyncio.run(say_goodbye_internal())

    # 2. DAS AUFRÄUMEN (Fenster schliessen)
    for title in targets:
        try:
            windows = gw.getWindowsWithTitle('')
            for win in windows:
                try:
                    if title.lower() in win.title.lower():
                        print(f"Schliesse Fenster: {win.title}")
                        win.close()
                except: continue
        except: continue

    # 3. DIE CHIRURGISCHE REINIGUNG (Sich selbst verschonen)
    print("[!] Gezielte Prozess-Terminierung...")
    current_pid = os.getpid() 
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Killt alle anderen Python-Skripte (Butler, Router etc.)
            if proc.info['name'] and "python" in proc.info['name'].lower() and proc.info['pid'] != current_pid:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Powershell darf komplett sterben (löst Dateisperren)
    os.system("taskkill /f /im powershell.exe >nul 2>&1")
    
    # 4. FINALE DATEI-HYGIENE (Der letzte Besenstrich)
    # Wir löschen alle potenziellen Sprach-Leichen
    for f in ["current_voice_GEE.mp3", "goodbye_GEE.mp3", "current_voice_META.mp3"]:
        path = os.path.abspath(f)
        if os.path.exists(path):
            try: 
                os.remove(path)
                print(f"Gereinigt: {f}")
            except: 
                pass

    print("[DONE] Das schallisolierte Zimmer ist gereinigt. Lichter aus.")

if __name__ == "__main__":
    run_shutdown()

