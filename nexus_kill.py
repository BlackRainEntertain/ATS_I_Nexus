import pygetwindow as gw
import os
import time
import asyncio
import edge_tts
import subprocess

# --- DIE ABSCHIEDS-INJEKTION ---
async def say_goodbye_internal():
    # Wir lassen Katja das letzte Wort, sie ist die Stimme des Nexus
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
    # Meta wurde hier als "META_AI NEXUS" (oder der Titel deiner start_meta.bat) hinzugefügt
    targets = [
        "ATSI'S NEXUS", 
        "GEE_AI NEXUS", 
        "VORTEX",
        "AUDIO_MASTER_BUTLER", 
        "NEXUS_ALL_SYSTEMS_GO", 
        "cmd.exe"
    ]
    
    print("[!] Einleiten der Tiefenreinigung (Inklusive Meta-Vortex)...")

    # 1. DER ABSCHIED
    asyncio.run(say_goodbye_internal())

    # 2. DAS AUFRÄUMEN (Fenster schliessen)
    for title in targets:
        try:
            windows = gw.getWindowsWithTitle('')
            for win in windows:
                try:
                    # Case-insensitive Vergleich für maximale Trefferrate
                    if title.lower() in win.title.lower():
                        print(f"Schliesse Fenster: {win.title}")
                        win.close()
                except: continue
        except: continue

    # 3. DIE EISENFAUST (Prozesse beenden)
    # Wir killen alles, was Python oder PowerShell heißt, um sicherzugehen
    print("[!] Letzte Bereinigung der Prozesse...")
    os.system("taskkill /f /im powershell.exe >nul 2>&1")
    os.system("taskkill /f /im python.exe /t >nul 2>&1")

    print("[DONE] Das schallisolierte Zimmer ist gereinigt. Lichter aus.")

if __name__ == "__main__":
    run_shutdown()



