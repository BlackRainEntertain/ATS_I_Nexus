import pygetwindow as gw
import time
import ctypes
import os
import subprocess

def set_always_on_top(title_part):
    windows = [w for w in gw.getWindowsWithTitle('') if title_part.lower() in w.title.lower()]
    for win in windows:
        ctypes.windll.user32.SetWindowPos(win._hWnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

def move_window(target_title, x, y, width, height, exact=False):
    all_wins = gw.getWindowsWithTitle('')
    # Wir suchen jetzt smarter: Wenn exakt gewünscht, prüfen wir ob der Titel mit dem Wort STARTET
    if exact:
        windows = [w for w in all_wins if w.title.strip().startswith(target_title)]
    else:
        windows = [w for w in all_wins if target_title.lower() in w.title.lower()]
    
    if windows:
        win = windows[0] # Nimm den ersten Treffer
        try:
            win.restore()
            win.moveTo(int(x), int(y))
            win.resizeTo(int(width), int(height))
            print(f"[CHECK] {target_title} positioniert.")
        except: pass

# --- BASIS DATEN ---
OFFSET_X, MON2_W = 2560, 1920
X_START, LM_H = OFFSET_X + MON2_W - 688, 414
W_CLEAN, GAP_CORR = 205, 15 
W_LAVA, W_QUEUE_SLIM = 150, 193
X_LM = X_START
X_NEXUS = X_LM + W_CLEAN - GAP_CORR
X_QUEUE = X_NEXUS + W_CLEAN - GAP_CORR
X_LAVA = X_QUEUE + W_QUEUE_SLIM - GAP_CORR + 8

def wake_trinity():
    """Öffnet Ordner NUR, wenn wirklich kein Fenster mit diesem Namen existiert."""
    trinity = {
        "LM Projekte": r"C:\Users\René\Desktop\LM Projekte",
        "Nexus": r"C:\Users\René\Desktop\LM Projekte\Nexus",
        "_Voice_Queue": r"C:\Users\René\Desktop\LM Projekte\Nexus\_Voice_Queue"
    }
    all_titles = [w.title for w in gw.getWindowsWithTitle('')]
    for title, path in trinity.items():
        # Suche ob der Titel irgendwo in den offenen Fenstern vorkommt
        exists = any(title in t for t in all_titles)
        if not exists:
            print(f"[!] {title} fehlt im Orbit. Starte Explorer...")
            subprocess.Popen(f'explorer "{path}"')
            time.sleep(1.5)

if __name__ == "__main__":
    print("K.I.T.T. Ultima: Zerstöre Explorer-Hydra...")
    wake_trinity()
    time.sleep(2.0)

    # 1. KIs
    move_window("ATSI_NEXUS_RECEIVER", OFFSET_X - 13, 0, 658, 548)
    move_window("GEE_AI_NEXUS", OFFSET_X - 13, 540, 658, 548)
    move_window("VORTEX", OFFSET_X + 625, 0, 625, 548)
    move_window("GPT_NEXUS", OFFSET_X + 625, 540, 625, 548)
    
    # 2. TRINITY (Smarte Exaktheit)
    move_window("LM Projekte", X_LM, 0, W_CLEAN, LM_H, exact=True)
    move_window("Nexus", X_NEXUS, 0, W_CLEAN, LM_H, exact=True)
    move_window("_Voice_Queue", X_QUEUE, 0, W_QUEUE_SLIM, LM_H, exact=True)
    move_window("NEXUS_LAVA", X_LAVA, 0, W_LAVA, LM_H)
    
    # 3. BUTLER & VM
    move_window("AUDIO_MASTER_BUTLER", OFFSET_X + MON2_W - 487, 1080 - 414, 487, 414)
    move_window("Voicemeeter", OFFSET_X + MON2_W - 1022 - 123, 1080 - 625 - 54, 1022, 625)

    time.sleep(0.5)
    targets = ["ATSI_NEXUS_RECEIVER", "GEE_AI_NEXUS", "GPT_NEXUS", "VORTEX", "LM Projekte", "Nexus", "_Voice_Queue", "NEXUS_LAVA", "AUDIO_MASTER_BUTLER"]
    for t in targets: set_always_on_top(t)
    print("\n[DONE] Matrix bündig. Keine Hydra-Brut mehr.")
