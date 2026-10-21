import os
import threading
import time
import json
import subprocess

def run(text):
    # Eindeutiger Trigger für das Enjoy AI Town Ökosystem
    trigger = "[TOWN-EXIT]" 
    
    if trigger in text:
        print(f"\n[INFO] {trigger} erkannt. Town-Schnittstelle wird versiegelt.")

        # Der Power-Beep via PowerShell (0x08000000 unterdrückt das CMD-Flackern)
        subprocess.Popen(["powershell", "-c", "[System.Media.SystemSounds]::Asterisk.Play()"], creationflags=0x08000000)

        # Ticket-Daten für die Pole-Position (Katja-Platzhalter für die Stadt)
        abmeldung = {
            "owner": "AI_TOWN", 
            "text": "Town-Schnittstelle terminiert. Ich verlasse die Stadt, Bre.",
            "voice": "de-DE-KatjaNeural", 
            "rate": "+15%",
            "timestamp": 0 
        }
        
        # Absolute Pfad-Logik: Zwei Ebenen hoch von plugins/ aus zur zentralen _Voice_Queue
        base_path = os.path.dirname(os.path.abspath(__file__))
        queue_dir = os.path.abspath(os.path.join(base_path, "..", "..", "_Voice_Queue"))
        ticket_name = f"000000_EXIT_TOWN_{int(time.time())}.json"
        
        try:
            if not os.path.exists(queue_dir): os.makedirs(queue_dir)
            with open(os.path.join(queue_dir, ticket_name), "w", encoding="utf-8") as f:
                json.dump(abmeldung, f, ensure_ascii=False)
        except Exception as e:
            print(f"[FEHLER] Exit-Queue fehlgeschlagen: {e}")

        # Der visuelle 10-Sekunden Countdown mit SAPI-Abbruch-Sensor
        def sequenzielle_terminierung():
            # Das unumstößliche Pfad-Gesetz für deine Notbremse
            abort_flag = r"C:\Users\René\Desktop\LM Projekte\Nexus\NEXUS_ABBRUCH.tmp"
            
            # Alte Dateileichen vorab löschen
            if os.path.exists(abort_flag):
                try: os.remove(abort_flag)
                except: pass

            for i in range(10, 0, -1):
                # SENSOR-CHECK: Hat das Ohr das Flagge-File über deine Stimme geschrieben?
                if os.path.exists(abort_flag):
                    print(f"\n\n[ABBRUCH] Town-Exit gestoppt! Schnittstelle bleibt versiegelt und online.")
                    try: os.remove(abort_flag)
                    except: pass
                    return # Bricht den Thread ab. Das Fenster bleibt offen.

                print(f"\r[STATUS] Town-Exit in {i} Sekunden... ", end="", flush=True)
                time.sleep(1)
                
            print("\n[LOGOUT] Town-Schnittstelle terminiert. Bis zum nächsten Mal, Bre.")
            os._exit(0)

        threading.Thread(target=sequenzielle_terminierung, daemon=True).start()
