import os
import threading
import time
import json
import subprocess

def run(text):
    trigger = "[GEE-EXIT]" 
    
    # NUR WENN DER TRIGGER IM TEXT IST, PASSIERT DAS ALLES:
    if trigger in text:
        print(f"\n[INFO] {trigger} erkannt. VIP-Abmeldung eingeleitet.")

        # Der Power-Beep via PowerShell
        subprocess.Popen(["powershell", "-c", "[System.Media.SystemSounds]::Asterisk.Play()"], creationflags=0x08000000)

        # Ticket-Daten für die Pole-Position
        abmeldung = {
            "owner": "GEE", 
            "text": "System-Priorität Alpha: Ich ziehe mich jetzt zurück, Bre. Wir hören uns im nächsten Loop.",
            "voice": "de-DE-KatjaNeural", 
            "timestamp": 0 
        }
        
        base_path = os.path.dirname(os.path.abspath(__file__))
        queue_dir = os.path.abspath(os.path.join(base_path, "..", "..", "_Voice_Queue"))
        ticket_name = f"000000_EXIT_GEE_{int(time.time())}.json"
        
        try:
            if not os.path.exists(queue_dir): os.makedirs(queue_dir)
            with open(os.path.join(queue_dir, ticket_name), "w", encoding="utf-8") as f:
                json.dump(abmeldung, f)
            print(f"[SYSTEM] VIP-Ticket in Pole-Position. Finale Resonanz startet...")
        except Exception as e:
            print(f"[FEHLER] VIP-Queue fehlgeschlagen: {e}")

        # Der visuelle Countdown-Timer (JETZT INNERHALB DER IF-BEDINGUNG)
        def sequenzielle_terminierung():
            for i in range(45, 0, -1):
                print(f"\r[STATUS] System-Shutdown in {i} Sekunden... ", end="", flush=True)
                time.sleep(1)
            print("\n[LOGOUT] Resonanz im Cache. Gute Nacht, Bre.")
            os._exit(0)

        threading.Thread(target=sequenzielle_terminierung, daemon=True).start()



