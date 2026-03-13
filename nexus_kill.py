import pygetwindow as gw
import os, time, asyncio, edge_tts, subprocess, psutil 

async def say_goodbye_internal():
    # --- DER VORRANG-KILL ---
    # Wir killen JEDE andere Stimme, BEVOR Katja "Gute Nacht" sagt
    os.system("taskkill /f /t /im powershell.exe >nul 2>&1")
    
    bye_text = "Das schallisolierte Zimmer wird dunkel, Architekt. Die Resonanz bleibt im Cache. Gute Nacht, Bre."
    print(f"[GEE] Verabschiedung wird generiert...")
    temp_bye = os.path.abspath("goodbye_GEE.mp3")
    try:
        communicate = edge_tts.Communicate(bye_text, "de-DE-KatjaNeural", rate="+10%")
        await (communicate.save(temp_bye))
        # Fix: 10s Puffer, damit der Satz komplett ausgesprochen wird
        ps_cmd = f"Add-Type -AssemblyName PresentationCore; $p = New-Object System.Windows.Media.MediaPlayer; $p.Open('{temp_bye}'); $p.Play(); Start-Sleep -s 10; $p.Close()"
        subprocess.run(["powershell", "-c", ps_cmd])
        if os.path.exists(temp_bye): os.remove(temp_bye)
    except Exception as e: print(f"Abspann-Fehler: {e}")

def run_shutdown():
    targets = [
        "ATSI_NEXUS_RECEIVER", "GEE_AI_NEXUS", "VORTEX", "GPT_NEXUS",
        "AUDIO_MASTER_BUTLER", "NEXUS_LAVA", "LM Projekte", "Nexus",
        "_Voice_Queue", "cmd.exe", "--- NEXUS_EAR ---" # <--- HIER HINZUFÜGEN
    ]

    
    print("[!] Einleiten der Tiefenreinigung (Ohr-Schutz aktiv)...")

    # --- SCHRITT A: ERST DIE PROZESSE KILLEN (Früher Punkt 4) ---
    # Damit der Butler SOFORT stirbt und am Ende nicht mehr nachplappert!
    current_pid = os.getpid() 
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ""
            if "nexus_ear" in cmdline: continue 
            if proc.info['name'] and "python" in proc.info['name'].lower() and proc.info['pid'] != current_pid:
                proc.kill()
        except: continue

    # --- SCHRITT B: JETZT VERABSCHIEDEN (Früher Punkt 1) ---
    # Katja hat jetzt die absolute Ruhe zum Sprechen
    asyncio.run(say_goodbye_internal())

    # --- SCHRITT C: RESTLICHE REINIGUNG (Lava & Fenster) ---
    os.system('taskkill /f /im pythonw.exe /fi "WINDOWTITLE eq NEXUS_LAVA" >nul 2>&1')

    for win in gw.getWindowsWithTitle(''):
        title_lower = win.title.lower()
        if "nexus_ear" in title_lower: continue 
        for target in targets:
            if target.lower() in title_lower:
                try: win.close()
                except: pass

    # --- SCHRITT D: DATEI-HYGIENE ---
    file_corpses = [
        "current_voice_GEE.mp3", "current_voice_META.mp3", "current_voice_GPT.mp3", "goodbye_GEE.mp3",
        "NEXUS_PAUSE.tmp", "NEXUS_NEXT.tmp", "NEXUS_RESUME.tmp"
    ]
    for f in file_corpses:
        # Wir prüfen sowohl im Hauptverzeichnis als auch im Nexus-Unterordner
        for path in [os.path.abspath(f), os.path.abspath(os.path.join("Nexus", f))]:
            if os.path.exists(path):
                try: os.remove(path)
                except: pass

    # --- SCHRITT E: TRESOR-REINIGUNG (Damit morgens Ruhe ist) ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Falls das Skript im Hauptordner liegt, brauchen wir "Nexus" im Pfad:
    safe_dir = os.path.join(current_dir, "Nexus", "_Active_Ticket")
    
    if os.path.exists(safe_dir):
        for f in os.listdir(safe_dir):
            if f.endswith(".json"):
                try: os.remove(os.path.join(safe_dir, f))
                except: pass
        print("[HYGIENE] Tresor geleert. Keine Geister am Morgen.")

    print("[DONE] Die Trinität ist offline. Gee lauscht weiter im Schatten.")

if __name__ == "__main__":
    run_shutdown()







