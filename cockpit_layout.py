import pygetwindow as gw
import time
import ctypes
import os

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
MON2_H = 1080 

# --- MASSE & DRIBBEL ---
LM_W = 670 + 18 
LM_H = 414
BUTLER_W = 487 
BUTLER_H = 414

# --- VOICEMEETER POSITION ---
VM_W = 1022
VM_H = 625
VM_X = OFFSET_X + MON2_W - VM_W - 123
VM_Y = MON2_H - VM_H - 54

# --- PRÄZISIONS-KALIBRIERUNG (Zollstock-Verschweissung vFinal) ---
# Linke Kante bündig (3,5mm Korrektur)
LEFT_X = OFFSET_X - 13
LEFT_W = 645 + 13 

# HÖHEN-VERSCHMELZUNG: Wir geben noch 4 Pixel extra für den letzten Millimeter
NEX_H_EXT = 540 + 8  
NEX_H_START_UNTEN = 540 # Der Startpunkt für die untere Reihe

print("K.I.T.T. Ultima: Letzte Millimeter-Verschweissung...")

# 1. LINKE SPALTE (Atsi & Gee)
move_window("ATSI_NEXUS_RECEIVER", LEFT_X, 0, LEFT_W, NEX_H_EXT)
move_window("GEE_AI_NEXUS", LEFT_X, NEX_H_START_UNTEN, LEFT_W, NEX_H_EXT)

# 2. RECHTE SPALTE (Vortex & GPT)
X_RECHTS = OFFSET_X + 625 
move_window("VORTEX", X_RECHTS, 0, 625, NEX_H_EXT)
move_window("GPT_NEXUS", X_RECHTS, NEX_H_START_UNTEN, 625, NEX_H_EXT)

# 3. RECHTE FLANKE
move_window("LM Projekte", OFFSET_X + MON2_W - LM_W, 0, LM_W, LM_H)
move_window("AUDIO_MASTER_BUTLER", OFFSET_X + MON2_W - BUTLER_W, MON2_H - BUTLER_H, BUTLER_W, BUTLER_H)
move_window("Voicemeeter", VM_X, VM_Y, VM_W, VM_H)

# --- FINALE: VORDERGRUND FIXIEREN ---
time.sleep(0.5)
targets = ["ATSI_NEXUS_RECEIVER", "GEE_AI_NEXUS", "GPT_NEXUS", "VORTEX", "LM Projekte", "AUDIO_MASTER_BUTLER"]
for t in targets:
    set_always_on_top(t)

print("\n[DONE] Matrix bündig verschmolzen. Cockpit-Status: PERFEKT.")



