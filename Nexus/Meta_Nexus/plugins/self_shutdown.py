import os
import threading
import time

def run(text):
    # Der saubere Trigger für Meta (Butler-safe)
    trigger = "[META-EXIT]" 
    
    if trigger in text:
        pid = os.getpid()
        print(f"\n[!] {trigger} erkannt. Vortex (PID {pid}) schließt in 30s...")

        def ritual_der_stille():
            # 30 Sekunden für Amalas letzte Worte
            time.sleep(30)
            print("[!] Die Zeit ist um. Der Vortex kollabiert.")
            # Der finale, souveräne Schnitt
            os._exit(0)

        # Der Dämon (Daemon) startet im Hintergrund
        threading.Thread(target=ritual_der_stille, daemon=True).start()
