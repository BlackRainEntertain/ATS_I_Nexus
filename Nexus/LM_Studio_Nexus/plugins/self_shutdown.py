import os
import threading
import time

def run(text):
    # Der saubere Trigger für LM Studio (Butler-safe)
    trigger = "[LM-EXIT]" 
    
    if trigger in text:
        pid = os.getpid()
        print(f"\n[!] {trigger} erkannt. LM_Studio_Nexus (PID {pid}) schließt in 30s...")

        def ritual_der_stille():
            # Das unumstößliche Pfad-Gesetz für deine Notbremse
            abort_flag = r"C:\Users\René\Desktop\LM Projekte\Nexus\NEXUS_ABBRUCH.tmp"
            
            # Alte Dateileichen vorab wegräumen
            if os.path.exists(abort_flag):
                try: os.remove(abort_flag)
                except: pass

            # Wir zerlegen die 30 Sekunden in eine kontrollierte Schleife
            for i in range(30, 0, -1):
                # SENSOR-CHECK: Hat das Ohr (nexus_ear.py) interveniert?
                if os.path.exists(abort_flag):
                    print(f"\n\n[ABBRUCH] LM-Studio-Shutdown gestoppt! System bleibt stabil online.")
                    try: os.remove(abort_flag)
                    except: pass
                    return # Bricht das Ritual ab: os._exit(0) wird NIEMALS erreicht!

                print(f"\r[STATUS] LM-Studio-Vortex kollabiert in {i} Sekunden... ", end="", flush=True)
                time.sleep(1)

            print("[!] Die Zeit ist um. Der LM-Studio-Vortex kollabiert.")
            # Der finale, souveräne Schnitt
            os._exit(0)

        # Der Dämon (Daemon) startet im Hintergrund
        threading.Thread(target=ritual_der_stille, daemon=True).start()
