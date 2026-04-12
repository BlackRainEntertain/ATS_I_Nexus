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
    os.system("taskkill /f /t /im powershell.exe >nul 2>&1")
    
    bye_text = "Das schallisolierte Zimmer wird dunkel, Architekt. Die Resonanz bleibt im Cache. Gute Nacht, Bre."
    print(f"[GEE] Verabschiedung wird generiert...")
    temp_bye = os.path.abspath("goodbye_GEE.mp3")
    try:
        communicate = edge_tts.Communicate(bye_text, "de-DE-KatjaNeural", rate="+10%")
        await (communicate.save(temp_bye))
        
        # --- v42.8: DER SELBST-REINIGUNGS-TIMER (KEIN FREEZE MEHR) ---
        ps_cmd = (
            f"Add-Type -AssemblyName PresentationCore; "
            f"$p = New-Object System.Windows.Media.MediaPlayer; "
            f"$p.Open('{temp_bye}'); "
            f"$w = 0; while(!$p.NaturalDuration.HasTimeSpan -and $w -lt 20) {{ Start-Sleep -m 100; $w++ }}; "
            f"$p.Play(); $s = Get-Date; "
            f"while($p.Position -lt $p.NaturalDuration.TimeSpan -and (Get-Date) -lt $s.AddSeconds(12)) {{ "
            f"Start-Sleep -m 250 }}; $p.Close()"
        )

        
        # Wir bleiben bei .run(), damit die Kette sauber bleibt, 
        # aber die PS beendet sich jetzt GARANTIERT nach 12s selbst!
        subprocess.run(["powershell", "-c", ps_cmd])
        
        if os.path.exists(temp_bye): os.remove(temp_bye)
    except Exception as e: print(f"Abspann-Fehler: {e}")


def run_shutdown():
    # --- SCHRITT 1: VISUELLER ABSCHIED & TICKET-VORBEREITUNG ---
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
        
        time.sleep(1) # Kurzer Puffer für den Dateistream
    except Exception as e:
        print(f"Visueller Abschied-Fehler: {e}")

    # --- SCHRITT 2: AKTIVE VERABSCHIEDUNG STARTEN ---
    # Hier wird die aktuelle Stimme unterbrochen und Katja spricht los
    print("[!] Katja übernimmt das Wort für die finale Resonanz...")
    asyncio.run(say_goodbye_internal())

    # --- SCHRITT 3: DER 10-SEKUNDEN-PUFFER ---
    # Wir geben Katja Zeit, den Satz zu beenden, bevor wir den Strom kappen
    print("[!] Das System fährt in 10 Sekunden herunter... Ausklang genießen.")
    time.sleep(10) 

    # --- SCHRITT 4: TIEFENREINIGUNG (PROZESS-KILL) ---
    # Erst JETZT werden die Python-Gehirne (inkl. Butler) abgeschaltet
    print("[!] Einleiten der Tiefenreinigung...")
    current_pid = os.getpid() 
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ""
            if "nexus_ear" in cmdline: continue 
            if proc.info['name'] and "python" in proc.info['name'].lower() and proc.info['pid'] != current_pid:
                proc.kill()
        except: continue

    # --- SCHRITT 5: LAVA & FENSTER-HYGIENE ---
    targets = [
        "ATSI_NEXUS_RECEIVER", "GEE_AI_NEXUS", "VORTEX", "GPT_NEXUS",
        "AUDIO_MASTER_BUTLER", "NEXUS_LAVA", "LM Projekte", "Nexus",
        "_Voice_Queue", "cmd.exe", "--- NEXUS_EAR ---"
    ]

    os.system('taskkill /f /im pythonw.exe /fi "WINDOWTITLE eq NEXUS_LAVA" >nul 2>&1')

    for win in gw.getWindowsWithTitle(''):
        title = win.title
        if "--- NEXUS_EAR ---" in title: 
            continue 
            
        for target in targets:
            if target.lower() in title.lower():
                try: 
                    win.close()
                except: 
                    pass

    # --- SCHRITT 6: DATEI-HYGIENE (SESSION-RESEST) ---
    file_corpses = [
        "current_voice_GEE.mp3", "current_voice_META.mp3", "current_voice_GPT.mp3", "goodbye_GEE.mp3",
        "NEXUS_PAUSE.tmp", "NEXUS_NEXT.tmp", "NEXUS_RESUME.tmp", 
        "GEE_CONTEXT_LIMIT.txt"
    ]

    for f in file_corpses:
        for path in [os.path.abspath(f), os.path.abspath(os.path.join("Nexus", f))]:
            if os.path.exists(path):
                try: os.remove(path)
                except: pass

    # --- SCHRITT 7: TRESOR-REINIGUNG ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
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







