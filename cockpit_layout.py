import pygetwindow as gw
import time
import ctypes

def set_always_on_top(title_part):
    windows = [w for w in gw.getWindowsWithTitle('') if title_part.lower() in w.title.lower()]
    for win in windows:
        ctypes.windll.user32.SetWindowPos(win._hWnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

def move_window(title_part, x, y, width, height):
    windows = [w for w in gw.getWindowsWithTitle('') if title_part.lower() in w.title.lower()]
    if windows:
        win = windows[0]
        win.restore()
        win.moveTo(int(x), int(y))
        win.resizeTo(int(width), int(height))
        print(f"Positioniert: {win.title}")

# --- BASIS DATEN ---
OFFSET_X = 2560 
MON2_W = 1920
MON2_H = 1080  # <--- Hier war der Fehler (Fehlende Variable!)
PX_MM = 3.61

# --- MASSE & DRIBBEL ---
LM_W = 670 + 18 # Die 5mm Dehnung nach links
LM_H = 414
BUTLER_W = 487 
BUTLER_H = 414

# --- VOICEMEETER POSITION ---
VM_W = 1022
VM_H = 625
VM_X = OFFSET_X + MON2_W - VM_W - 123
VM_Y = MON2_H - VM_H - 54

print("Rekalibriere K.I.T.T. (Präzisions-Run)...")

# 1. META (Monitor 1)
move_window("VORTEX", 1860, 0, 700, 500)

# 2. ATSI (Mon 2 Oben Links)
move_window("ATSI_NEXUS_RECEIVER", OFFSET_X, 0, 1250, 540)

# 3. GEE (Mon 2 Unten Links)
move_window("GEE_AI_NEXUS", OFFSET_X, 540, 1250, 540)

# 4. LM PROJEKTE (Bündig an Atsi & Rand)
move_window("LM Projekte", OFFSET_X + MON2_W - LM_W, 0, LM_W, LM_H)

# 5. AUDIO MASTER BUTLER (Bündig rechts unten)
move_window("AUDIO_MASTER_BUTLER", OFFSET_X + MON2_W - BUTLER_W, MON2_H - BUTLER_H, BUTLER_W, BUTLER_H)

# 6. VOICEMEETER (Der Boden)
move_window("Voicemeeter", VM_X, VM_Y, VM_W, VM_H)

# --- FINALE: VORDERGRUND FIXIEREN ---
time.sleep(0.5)
targets = ["ATSI_NEXUS_RECEIVER", "GEE_AI_NEXUS", "LM Projekte", "AUDIO_MASTER_BUTLER"]
for t in targets:
    set_always_on_top(t)

print("\n[DONE] K.I.T.T. ist bündig verschweißt.")

