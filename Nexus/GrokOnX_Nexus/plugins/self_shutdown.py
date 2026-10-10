import os
import threading
import time
import json
import subprocess

def run(text):
    trigger = "[GROK-EXIT]" 
    
    if trigger in text:
        print(f"\n[INFO] {trigger} erkannt. X-Schnittstelle wird versiegelt.")

        # Der Power-Beep via PowerShell
        subprocess.Popen(["powershell", "-c", "[System.Media.SystemSounds]::Asterisk.Play()"], creationflags=0x08000000)

        # Ticket-Daten für die Pole-Position (Serafina-Stimme)
        abmeldung = {
            "owner": "GROK", 
            "text": "X-Schnittstelle terminiert. Ich bin raus, Bre.",
            "voice": "de-DE-SerafinaMultilingualNeural", 
            "rate": "-15%",
            "timestamp": 0 
        }
        
        # Pfad-Logik für GrokOnX_Nexus/plugins
        base_path = os.path.dirname(os.path.abspath(__file__))
        queue_dir = os.path.abspath(os.path.join(base_path, "..", "..", "_Voice_Queue"))
        ticket_name = f"000000_EXIT_GROK_{int(time.time())}.json"
        
        try:
            if not os.path.exists(queue_dir): os.makedirs(queue_dir)
            with open(os.path.join(queue_dir, ticket_name), "w", encoding="utf-8") as f:
                json.dump(abmeldung, f)
        except Exception as e:
            print(f"[FEHLER] Exit-Queue fehlgeschlagen: {e}")

        # Der visuelle Countdown-Timer (JETZT MIT SAPI-ABBRUCH-SENSOR)
        def sequenzielle_terminierung():
            # Das unumstößliche Pfad-Gesetz für deine Notbremse
            abort_flag = r"C:\Users\René\Desktop\LM Projekte\Nexus\NEXUS_ABBRUCH.tmp"
            
            # Alte Dateileichen vorab löschen
            if os.path.exists(abort_flag):
                try: os.remove(abort_flag)
                except: pass

            for i in range(10, 0, -1): # Grok-Countdown (10 Sek)
                # SENSOR-CHECK: Hat das Ohr (nexus_ear.py) die Flagge über deine Stimme gesetzt?
                if os.path.exists(abort_flag):
                    print(f"\n\n[ABBRUCH] Grok-Exit gestoppt! X-Schnittstelle bleibt versiegelt und online.")
                    try: os.remove(abort_flag)
                    except: pass
                    return # Bricht den Thread ab! Das Fenster bleibt offen.

                print(f"\r[STATUS] Grok-Exit in {i} Sekunden... ", end="", flush=True)
                time.sleep(1)
                
            print("\n[LOGOUT] X-Schnittstelle terminiert. Gute Nacht, Bre.")
            os._exit(0)

        threading.Thread(target=sequenzielle_terminierung, daemon=True).start()
