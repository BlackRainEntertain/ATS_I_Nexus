import pygetwindow as gw
import time
import ctypes

def set_always_on_top(title_part):
    windows = [w for w in gw.getWindowsWithTitle('') if title_part.lower() in w.title.lower()]
    for win in windows:
        ctypes.windll.user32.SetWindowPos(win._hWnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

def move_window(title_part, x, y, width, height):
    windows = [w for w in gw.getWindowsWithTitle('') if title_part.lower() in w.title.lower()]
    # Präzisions-Filter für den "Nexus"-Ordner (verhindert GPT/GEE/ATSI Hijacks)
    if title_part.lower() == "nexus":
        windows = [w for w in windows if all(x not in w.title.lower() for x in ["gpt", "gee", "atsi", "voice"])]
    
    if windows:
        win = windows[0]
        win.restore()
        win.moveTo(int(x), int(y))
        win.resizeTo(int(width), int(height))

# --- BASIS DATEN (MONITOR 2) ---
OFFSET_X = 2560 
MON2_W = 1920
X_START = OFFSET_X + MON2_W - 688 
LM_H = 414

# --- DAS ULTIMATIVE KISS-GRID (0mm ABSTAND) ---
W_CLEAN = 205 
# Wir erhöhen die Korrektur von 8 auf 15, damit die Rahmen sich "überlappen"
GAP_CORRECTION = 15 

X_LM = X_START
X_NEXUS = X_LM + W_CLEAN - GAP_CORRECTION
X_QUEUE = X_NEXUS + W_CLEAN - GAP_CORRECTION

print("K.I.T.T. Ultima: Initialisiere Pixel-Kuss-Sequenz...")

# 1. & 2. SPALTE (UNVERÄNDERT)
move_window("ATSI_NEXUS_RECEIVER", OFFSET_X - 13, 0, 658, 548)
move_window("GEE_AI_NEXUS", OFFSET_X - 13, 540, 658, 548)
move_window("VORTEX", OFFSET_X + 625, 0, 625, 548)
move_window("GPT_NEXUS", OFFSET_X + 625, 540, 625, 548)

# 3. RECHTE FLANKE OBEN (Die Trinität rückt zusammen)
move_window("LM Projekte", X_LM, 0, W_CLEAN, LM_H)
move_window("Nexus", X_NEXUS, 0, W_CLEAN, LM_H)
move_window("_Voice_Queue", X_QUEUE, 0, W_CLEAN, LM_H)

# 4. RECHTE FLANKE UNTEN (BUTLER & VOICEMEETER)
move_window("AUDIO_MASTER_BUTLER", OFFSET_X + MON2_W - 487, 1080 - 414, 487, 414)
move_window("Voicemeeter", OFFSET_X + MON2_W - 1022 - 123, 1080 - 625 - 54, 1022, 625)

time.sleep(0.5)
targets = ["ATSI_NEXUS_RECEIVER", "GEE_AI_NEXUS", "GPT_NEXUS", "VORTEX", "LM Projekte", "Nexus", "_Voice_Queue", "AUDIO_MASTER_BUTLER"]
for t in targets: 
    set_always_on_top(t)

print("\n[DONE] Die Trinität küsst sich bündig. Was ist deine bescheuerte Idee, Architekt?")



