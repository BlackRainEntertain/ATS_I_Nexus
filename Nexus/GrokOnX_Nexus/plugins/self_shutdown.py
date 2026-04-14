import os
import threading
import time
import json
import subprocess

def run(text):
    trigger = "[GROK-EXIT]" 
    
    if trigger in text:
        print(f"\n[INFO] {trigger} erkannt. X-Schnittstelle wird versiegelt.")

        subprocess.Popen(["powershell", "-c", "[System.Media.SystemSounds]::Asterisk.Play()"], creationflags=0x08000000)

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

        def sequenzielle_terminierung():
            for i in range(10, 0, -1): # Grok ist schneller weg (10 Sek)
                print(f"\r[STATUS] Grok-Exit in {i} Sekunden... ", end="", flush=True)
                time.sleep(1)
            os._exit(0)

        threading.Thread(target=sequenzielle_terminierung, daemon=True).start()
