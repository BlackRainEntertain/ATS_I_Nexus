import pygetwindow as gw
import time
import ctypes

# --- DIE EISERNE REGEL (Always on Top) ---
def set_always_on_top(title_part):
    windows = [w for w in gw.getWindowsWithTitle('') if title_part.lower() in w.title.lower()]
    for win in windows:
        # SetWindowPos: HWND_TOPMOST = -1
        ctypes.windll.user32.SetWindowPos(win._hWnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
        print(f"[TOP] {win.title} fixiert.")

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
PX_MM = 3.61 # 53cm x 30cm Matrix

# --- BERECHNUNG DER STAUCHUNG (35mm = 126px) ---
H_STAUCHUNG = 126 
NEW_H_PROJEKTE = 540 - H_STAUCHUNG

print("Starte K.I.T.T.-Kalibrierung (Monitor 2)...")

# 1. META (Monitor 1 - Oben Rechts)
move_window("VORTEX", 1860, 0, 700, 500)

# 2. ATSI (Oben Links auf Mon 2) - Bleibt Standard
move_window("ATSI_NEXUS_RECEIVER", OFFSET_X, 0, 1250, 540)

# 3. GEE (Unten Links auf Mon 2) - Bleibt Standard
move_window("GEE_AI_NEXUS", OFFSET_X, 540, 1250, 540)

# 4. LM PROJEKTE (Oben Rechts - GESTAUCHT)
# Y bleibt 0 (Oberkante fixiert), Höhe wird reduziert
move_window("LM Projekte", OFFSET_X + 1250 - 11, 0, 670, NEW_H_PROJEKTE)

# 5. AUDIO MASTER BUTLER (Unten Rechts - TIEFER GELEGT)
move_window("AUDIO_MASTER_BUTLER", OFFSET_X + 1250 + 199, 540 + 126, 670, 540)

# 6. VOICEMEETER (Hintergrund-Anzeige)
VM_W = 1022
VM_H = 625
VM_X = OFFSET_X + MON2_W - VM_W - 123
VM_Y = MON2_H - VM_H - 54
move_window("Voicemeeter", VM_X, VM_Y, VM_W, VM_H)

# --- FINALE: VORDERGRUND FIXIEREN ---
time.sleep(0.5)
set_always_on_top("ATSI_NEXUS_RECEIVER")
set_always_on_top("GEE_AI_NEXUS")
set_always_on_top("LM Projekte")
set_always_on_top("AUDIO_MASTER_BUTLER")

print("\n[DONE] Das 'L' ist ausgeschnitten. Voicemeeter liegt begraben.")

