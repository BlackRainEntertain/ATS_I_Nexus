import pygetwindow as gw
import os, time, asyncio, edge_tts, subprocess, psutil, json

async def say_goodbye_internal():
    # --- NEU: BUTLER-STRIKT-PAUSE (v42.9) ---
    # Wir legen den Butler schlafen, damit er keine neuen Tickets mehr anfasst
    try:
        with open(os.path.join("Nexus", "NEXUS_PAUSE.tmp"), "w") as f: 
            f.write("SHUTDOWN")
    except: pass

    # --- DER VORRANG-KILL (Bestehend) ---
    # Wir killen JEDE andere Stimme, BEVOR Katja "Gute Nacht" sagt
    os.system("taskkill /f /t /im powershell.exe /im pwsh.exe /im ffplay.exe >nul 2>&1")
    
    bye_text = "Das schallisolierte Zimmer wird dunkel, Architekt. Die Resonanz bleibt im Cache. Gute Nacht, Bre."
    print(f"[GEE] Verabschiedung wird generiert...")
    temp_bye = os.path.abspath("goodbye_GEE.mp3")
    try:
        communicate = edge_tts.Communicate(bye_text, "de-DE-KatjaNeural", rate="+10%")
        await (communicate.save(temp_bye))
        
        # --- TITAN-BYPASS v44.8 (FFPLAY-GOODBYE) ---
        # Wir nutzen ffplay direkt für die Verabschiedung (Lizenz-unabhängig)
        ffplay_path = os.path.join("Nexus", "ffplay.exe")
        if not os.path.exists(ffplay_path): ffplay_path = "ffplay.exe" # Fallback

        cmd = [ffplay_path, "-nodisp", "-autoexit", "-hide_banner", "-loglevel", "error", temp_bye]
        
        # Wir nutzen .run(), damit das Skript wartet, bis Katja fertig gesprochen hat
        subprocess.run(cmd, creationflags=0x08000000)

        
        if os.path.exists(temp_bye): os.remove(temp_bye)
    except Exception as e: print(f"Abspann-Fehler: {e}")


def run_shutdown():
    # --- SCHRITT 1: VISUELLER ABSCHIED ---
    try:
        q_path = os.path.join(os.getcwd(), "Nexus", "_Voice_Queue")
        if not os.path.exists(q_path): os.makedirs(q_path)
        
        ticket = {
            "text": "Das schallisolierte Zimmer wird dunkel, Architekt. Die Resonanz bleibt im Cache. Gute Nacht, Bre.",
            "owner": "NEXUS",
            "voice": "de-DE-KatjaNeural"
        }
        
        with open(os.path.join(q_path, "00_bye.json"), "w", encoding="utf-8") as f:
            json.dump(ticket, f)
        time.sleep(1) 
    except Exception as e:
        print(f"Visueller Abschied-Fehler: {e}")

    # --- SCHRITT 2: AKTIVE VERABSCHIEDUNG ---
    print("[!] Katja übernimmt das Wort...")
    asyncio.run(say_goodbye_internal())

    # --- SCHRITT 3: PUFFER ---
    print("[!] System-Stopp in 7,5 Sekunden...")
    time.sleep(7.5) 

    # --- SCHRITT 4: TIEFENREINIGUNG ---
    print("[!] Tiefenreinigung der Gehirne...")
    import psutil 
    current_pid = os.getpid() 
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ""
            
            # DER IDENTISCHE MOVE:
            # Wenn "nexus_ear" oder "explorer_exorcist" im Pfad auftauchen -> FINGER WEG
            if "nexus_ear" in cmdline or "explorer_exorcist" in cmdline: 
                continue 
            
            if proc.info['name'] and proc.info['name'].lower() in ["python.exe", "pythonw.exe", "pwsh.exe", "powershell.exe", "ffplay.exe"]:
                if proc.info['pid'] != current_pid:
                    proc.kill()

        except: continue

    # --- SCHRITT 5: FENSTER-HYGIENE (TITAN-Update) ---
    targets = [
        "AUDIO_MASTER_BUTLER_V43.9_TITAN_ULTRA", "ATSI_NEXUS", "GEE_AI_NEXUS", 
        "VORTEX", "GPT_NEXUS", "LAVA", "LM Projekte", "Nexus", 
        "_Voice_Queue", "cmd.exe"
    ]
    os.system('taskkill /f /im pythonw.exe /fi "WINDOWTITLE eq NEXUS_LAVA" >nul 2>&1')
    for win in gw.getWindowsWithTitle(''):
        title = win.title
        # SCHUTZ-ZONE: Weder das Ohr noch den Exorzisten schliessen
        if "--- NEXUS_EAR ---" in title or "--- EXPLORER_EXORZIST ---" in title:
            continue

        # ZUSATZ-SICHERUNG: Wenn "Google Chrome" oder "Vivaldi" im Titel steht -> SKIP
        if "Google Chrome" in title or "Vivaldi" in title or "Firefox" in title:
            continue
            
        for target in targets:
            if target.lower() in title.lower():
                try: win.close()
                except: pass


    # --- SCHRITT 6 & 7: DATEI- & TRESOR-HYGIENE ---
    print("[!] Bereinige Cache & Tresore...")
    file_corpses = ["current_voice_GEE.mp3", "current_voice_META.mp3", "current_voice_GPT.mp3", "goodbye_GEE.mp3", "NEXUS_PAUSE.tmp", "NEXUS_NEXT.tmp", "NEXUS_RESUME.tmp", "next_spoke.tmp"]
    
    for folder in [".", "Nexus", "Nexus/_Active_Ticket", "Nexus/_Voice_Queue"]:
        if not os.path.exists(folder): continue
        for f in os.listdir(folder):
            if f in file_corpses or f.endswith(".json") or f.endswith(".tmp"):
                try: os.unlink(os.path.join(folder, f))
                except: pass

    # --- SCHRITT 8: CHIRURGISCHE EXPLORER-REINIGUNG (RAM-Check) ---
    print("[!] Warte auf Hydra-Verwandlung...")
    time.sleep(2) # <--- WICHTIG: Gib Windows Zeit, die geschlossenen Fenster in Prozesse umzuwandeln
    
    print("[!] Exorziere Explorer-Zombies via RAM-Signatur...")
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == 'explorer.exe':
                mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                
                # Grenze 75MB: Killt die frischen Zombies (ca. 50-65MB)
                if mem_mb < 75: 
                    print(f"[KILL] Zombie-Explorer (PID {proc.info['pid']}, {mem_mb:.1f}MB) entfernt.")
                    proc.kill()
                else:
                    print(f"[KEEP] Shell/Desktop (PID {proc.info['pid']}, {mem_mb:.1f}MB) geschützt.")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    print("[DONE] System offline. Schlaf gut, Architekt.")


if __name__ == "__main__":
    run_shutdown()












