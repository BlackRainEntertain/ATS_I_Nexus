import psutil
import win32gui
import win32process
import time
import os

# --- KONFIGURATION (v2.4 - Die Titan-Lösung / FFPLAY-Update) ---
os.system("title --- DER_ULTIMATIVE_EXORZIST_SMART_v2.4 ---")
BASE_PATH = r"C:\Users\René\Desktop\LM Projekte"
SAFE_PATH = os.path.join(BASE_PATH, "Nexus", "_Active_Ticket")
INTERVAL = 240 

def butler_is_actually_speaking():
    """Prüft, ob der Butler wirklich gerade Audio via ffplay ausgibt."""
    # 1. Nur wenn ein Ticket im Safe-Ordner liegt, ist der Butler 'besetzt'
    try:
        if os.path.exists(SAFE_PATH) and len(os.listdir(SAFE_PATH)) > 0:
            return True
    except: pass

    # 2. Check: Läuft die ffplay-Engine?
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == "ffplay.exe":
                return True
        except:
            continue
    return False

def get_visible_pids():
    visible_pids = set()
    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            visible_pids.add(pid)
    win32gui.EnumWindows(enum_windows_proc, None)
    return visible_pids

def perform_exorcism():
    if butler_is_actually_speaking():
        print(f"[{time.strftime('%H:%M:%S')}] Butler aktiv (ffplay). Exorzismus verschoben.")
        return

    try:
        shell_hwnd = win32gui.GetShellWindow()
        _, shell_pid = win32process.GetWindowThreadProcessId(shell_hwnd)
    except: shell_pid = None

    visible_pids = get_visible_pids()
    target_shells = ['powershell.exe', 'pwsh.exe', 'explorer.exe', 'ffplay.exe']

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info['name'].lower()
            cmdline = " ".join(proc.info['cmdline'] if proc.info['cmdline'] else [])

            # --- DER SCHUTZSCHILD: Ignoriere den Butler und seine Audio-Engine ---
            if "master_butler.py" in cmdline or "ffplay.exe" in name:
                continue 

            if name in target_shells:
                pid = proc.info['pid']
                if pid == shell_pid or pid in visible_pids:
                    continue 

                print(f"[{time.strftime('%H:%M:%S')}] Banne Geist: {name} (PID {pid})")
                proc.terminate()
        except: continue

if __name__ == "__main__":
    print(f"Exorzismus-Protokoll v2.4 (Independent) aktiv. Intervall: {INTERVAL}s.")
    while True:
        perform_exorcism()
        time.sleep(INTERVAL)

