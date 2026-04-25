import psutil
import win32gui
import win32process
import time
import os

# --- KONFIGURATION (v2.2 - Smart Butler-Aware) ---
os.system("title --- DER_ULTIMATIVE_EXORZIST_SMART_v2.2 ---")
BASE_PATH = r"C:\Users\René\Desktop\LM Projekte"
QUEUE_PATH = os.path.join(BASE_PATH, "Nexus", "_Voice_Queue")
SAFE_PATH = os.path.join(BASE_PATH, "Nexus", "_Active_Ticket")
INTERVAL = 240 # 4 Minuten Intervall für maximale System-Ruhe

def butler_is_actually_speaking():
    """Prüft autonom, ob der Butler gerade arbeitet oder Audio ausgibt."""
    # 1. Check: Liegen Tickets in der Queue oder im Safe-Ordner?
    try:
        if os.path.exists(QUEUE_PATH) and len(os.listdir(QUEUE_PATH)) > 0:
            return True
        if os.path.exists(SAFE_PATH) and len(os.listdir(SAFE_PATH)) > 0:
            return True
    except: pass

    # 2. Check: Läuft ein aktiver Audio-Subprozess des Butlers?
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info.get('cmdline', []) if proc.info.get('cmdline') else "")
            # Sucht nach dem Herzschlag der Butler-Audio
            if "PresentationCore" in cmdline or "MediaPlayer" in cmdline:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
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
    # Butler-Schutzschild: Wenn er aktiv ist, wird der Scan komplett übersprungen
    if butler_is_actually_speaking():
        print(f"[{time.strftime('%H:%M:%S')}] Butler aktiv (Queue/Audio). Exorzismus verschoben.")
        return

    try:
        shell_hwnd = win32gui.GetShellWindow()
        _, shell_pid = win32process.GetWindowThreadProcessId(shell_hwnd)
    except:
        shell_pid = None

    visible_pids = get_visible_pids()
    target_shells = ['powershell.exe', 'pwsh.exe', 'explorer.exe']

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Re-Check während der Loop, falls der Butler plötzlich loslegt
            name = proc.info['name'].lower()
            if name in target_shells:
                pid = proc.info['pid']
                cmdline = " ".join(proc.info.get('cmdline', []) if proc.info.get('cmdline') else [])
                
                # Sicherheits-Schutz für Butler-Prozesse (Metadaten-Check)
                if "PresentationCore" in cmdline or "MediaPlayer" in cmdline:
                    continue 

                is_shell_main = (pid == shell_pid)
                is_visible = (pid in visible_pids)

                # Nur killen, wenn unsichtbar UND kein Haupt-Shell-Prozess
                if not is_shell_main and not is_visible:
                    print(f"[{time.strftime('%H:%M:%S')}] Banne Geist: {name} (PID {pid})")
                    proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

if __name__ == "__main__":
    print(f"Exorzismus-Protokoll v2.2 gestartet. Intervall: {INTERVAL}s.")
    print("Sicherheits-Anker: Butler-Aktivität hat Vorrang.")
    while True:
        perform_exorcism()
        time.sleep(INTERVAL)