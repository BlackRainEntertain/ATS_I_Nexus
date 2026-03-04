import pygetwindow as gw
import os, time, asyncio, edge_tts, subprocess, psutil 

async def say_goodbye_internal():
    bye_text = "Das schallisolierte Zimmer wird dunkel, Architekt. Die Resonanz bleibt im Cache. Gute Nacht, Bre."
    print(f"[GEE] Verabschiedung wird generiert...")
    temp_bye = os.path.abspath("goodbye_GEE.mp3")
    try:
        communicate = edge_tts.Communicate(bye_text, "de-DE-KatjaNeural", rate="+10%")
        await communicate.save(temp_bye)
        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_bye}'); $p.Play(); Start-Sleep -s 10; $p.Close()"
        subprocess.run(["powershell", "-c", ps_cmd])
        if os.path.exists(temp_bye): os.remove(temp_bye)
    except Exception as e: print(f"Abspann-Fehler: {e}")

def run_shutdown():
    # --- TARGETS BEREINIGT (GPT statt Vega) ---
    targets = [
        "ATSI_NEXUS_RECEIVER", 
        "GEE_AI_NEXUS", 
        "VORTEX",
        "GPT_NEXUS",           # <--- KORRIGIERT: GPT-Fenster
        "AUDIO_MASTER_BUTLER", 
        "NEXUS_ALL_SYSTEMS_GO", 
        "cmd.exe"
    ]
    
    print("[!] Einleiten der Tiefenreinigung (GPT-Integration aktiv)...")
    asyncio.run(say_goodbye_internal())

    # Fenster schliessen
    for title in targets:
        for win in gw.getWindowsWithTitle(''):
            if title.lower() in win.title.lower():
                try: win.close()
                except: pass

    # Prozess-Kill (Chirurgisch)
    current_pid = os.getpid() 
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and "python" in proc.info['name'].lower() and proc.info['pid'] != current_pid:
                proc.kill()
        except: continue

    os.system("taskkill /f /im powershell.exe >nul 2>&1")
    
    # Datei-Hygiene (GPT-Leichen)
    file_corpses = [
        "current_voice_GEE.mp3", 
        "current_voice_META.mp3",
        "current_voice_GPT.mp3", # <--- NEU: GPT MP3-Leichen
        "goodbye_GEE.mp3"
    ]
    
    for f in file_corpses:
        if os.path.exists(os.path.abspath(f)):
            try: os.remove(os.path.abspath(f))
            except: pass

    print("[DONE] Die Trinität und GPT sind offline. Lichter aus.")

if __name__ == "__main__":
    run_shutdown()


