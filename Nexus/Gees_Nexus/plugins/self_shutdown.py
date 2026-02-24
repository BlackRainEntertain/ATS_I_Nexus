import os
import threading
import time

def run(text):
    # Der Butler-safe Trigger (Bindestrich!)
    trigger = "GEE-EXIT" 
    
    if trigger in text:
        pid = os.getpid()
        # Diese Meldung erscheint sofort im schwarzen Fenster:
        print(f"\n[!] {trigger} erkannt. Phoenix-Sektor (PID {pid}) schliesst in 45s...")

        def ritual_der_stille():
            time.sleep(45)
            # Das reisst das Fenster mit in den Abgrund, wenn kein 'pause' in der .bat ist
            os._exit(0)

        threading.Thread(target=ritual_der_stille, daemon=True).start()
