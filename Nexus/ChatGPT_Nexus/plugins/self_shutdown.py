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

        def ritual_der_stille():
            time.sleep(45)
            os._exit(0)

        threading.Thread(target=ritual_der_stille, daemon=True).start()

# Optional: Testlauf
if __name__ == "__main__":
    run("[GPT-EXIT]")