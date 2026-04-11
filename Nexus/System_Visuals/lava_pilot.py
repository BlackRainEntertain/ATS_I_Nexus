import pygetwindow as gw
import ctypes
import time

def set_always_on_top(title_part):
    windows = [w for w in gw.getWindowsWithTitle('') if title_part.lower() in w.title.lower()]
    for win in windows:
        ctypes.windll.user32.SetWindowPos(win._hWnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

# Deine Cockpit-Mathematik
OFFSET_X, MON2_W = 2560, 1920
X_START = OFFSET_X + MON2_W - 688
W_CLEAN, GAP_CORR = 205, 15 
W_LAVA, W_QUEUE_SLIM = 150, 193
LM_H = 414

# Der exakte X_LAVA Vektor
X_LAVA = X_START + (W_CLEAN - GAP_CORR) + (W_CLEAN - GAP_CORR) + (W_QUEUE_SLIM - GAP_CORR) + 8

def position_lava():
    win = None
    # Warte kurz, bis das Fenster wirklich da ist
    for _ in range(10):
        wins = gw.getWindowsWithTitle('NEXUS_LAVA')
        if wins:
            win = wins[0]
            break
        time.sleep(0.5)

    if win:
        win.restore()
        win.moveTo(int(X_LAVA), 0)
        win.resizeTo(int(W_LAVA), int(LM_H))
        set_always_on_top("NEXUS_LAVA")
        print(f"[CHECK] NEXUS_LAVA bündig positioniert bei X: {X_LAVA}")

if __name__ == "__main__":
    position_lava()
