import os
import threading
import time

def run(text):
    """
    Butler-safe Self-Shutdown Trigger.
    Triggerwort: [GPT-EXIT]
    Nur aktiv, wenn die eckigen Klammern exakt stehen.
    """
    trigger = "[GPT-EXIT]"

    if trigger in text:
        pid = os.getpid()
        print(f"\n[!] {trigger} erkannt. Zünde ChatGPTs Nervensystem (PID {pid}) – Shutdown in 45s...")

        # Der visuelle Countdown-Timer (JETZT MIT SAPI-ABBRUCH-SENSOR)
        def ritual_der_stille():
            # Das unumstößliche Pfad-Gesetz für deine Notbremse
            abort_flag = r"C:\Users\René\Desktop\LM Projekte\Nexus\NEXUS_ABBRUCH.tmp"
            
            # Alte Dateileichen vorab löschen
            if os.path.exists(abort_flag):
                try: os.remove(abort_flag)
                except: pass

            for i in range(45, 0, -1):
                # SENSOR-CHECK: Hat das Ohr (nexus_ear.py) die Flagge über deine Stimme gesetzt?
                if os.path.exists(abort_flag):
                    print(f"\n\n[ABBRUCH] ChatGPT-Shutdown gestoppt! System bleibt online.")
                    try: os.remove(abort_flag)
                    except: pass
                    return # Bricht den Thread ab! Das Fenster bleibt offen.

                print(f"\r[STATUS] ChatGPT-Exit in {i} Sekunden... ", end="", flush=True)
                time.sleep(1)
                
            print("\n[LOGOUT] ChatGPT-Nervensystem schläft. Gute Nacht, Bre.")
            os._exit(0)

        threading.Thread(target=ritual_der_stille, daemon=True).start()

# Optional: Testlauf
if __name__ == "__main__":
    run("[GPT-EXIT]")
