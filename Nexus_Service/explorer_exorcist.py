import psutil
import win32gui
import win32process
import time
import os

# --- KONFIGURATION (v2.3 - Die Titan-Lösung) ---
os.system("title --- DER_ULTIMATIVE_EXORZIST_SMART_v2.3 ---")
BASE_PATH = r"C:\Users\René\Desktop\LM Projekte"
SAFE_PATH = os.path.join(BASE_PATH, "Nexus", "_Active_Ticket")
INTERVAL = 240 

def butler_is_actually_speaking():
    """Prüft, ob der Butler wirklich gerade Audio ausgibt."""
    # 1. Nur wenn ein Ticket im Safe-Ordner liegt, ist der Butler 'besetzt'
    try:
        if os.path.exists(SAFE_PATH) and len(os.listdir(SAFE_PATH)) > 0:
            return True
    except: pass

    # 2. Check: Läuft ein Audio-Kellner mit dem NEXUS-Namensschild?
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline'] if proc.info['cmdline'] else [])
            if "NEXUS_AUDIO_ENGINE" in cmdline:
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
        print(f"[{time.strftime('%H:%M:%S')}] Butler aktiv. Exorzismus verschoben.")
        return

    try:
        shell_hwnd = win32gui.GetShellWindow()
        _, shell_pid = win32process.GetWindowThreadProcessId(shell_hwnd)
    except: shell_pid = None

    visible_pids = get_visible_pids()
    target_shells = ['powershell.exe', 'pwsh.exe', 'explorer.exe']

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name'].lower()
            if name in target_shells:
                pid = proc.info['pid']
                if pid == shell_pid or pid in visible_pids:
                    continue 

                print(f"[{time.strftime('%H:%M:%S')}] Banne Geist: {name} (PID {pid})")
                proc.terminate()
        except: continue

if __name__ == "__main__":
    print(f"Exorzismus-Protokoll v2.3 aktiv. Intervall: {INTERVAL}s.")
    while True:
        perform_exorcism()
        time.sleep(INTERVAL)
