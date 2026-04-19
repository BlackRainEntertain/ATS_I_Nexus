import psutil
import win32gui
import win32process
import time
import os

os.system("title --- DER_ULTIMATIVE_EXORZIST_SAFE ---")

def get_visible_pids():
    visible_pids = set()
    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            visible_pids.add(pid)
    win32gui.EnumWindows(enum_windows_proc, None)
    return visible_pids

def perform_exorcism():
    try:
        shell_hwnd = win32gui.GetShellWindow()
        _, shell_pid = win32process.GetWindowThreadProcessId(shell_hwnd)
    except:
        shell_pid = None

    visible_pids = get_visible_pids()
    target_shells = ['powershell.exe', 'pwsh.exe', 'explorer.exe']

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info['name'].lower()
            if name in target_shells:
                pid = proc.info['pid']
                cmdline = " ".join(proc.info.get('cmdline', []) if proc.info.get('cmdline') else [])
                
                # --- DER BUTLER-SCHUTZSCHILD ---
                # Wenn im Befehl "MediaPlayer" oder "NaturalDuration" vorkommt, arbeitet der Butler gerade!
                if "PresentationCore" in cmdline or "MediaPlayer" in cmdline:
                    continue # Finger weg, das ist die laufende Audio!

                is_shell_main = (pid == shell_pid)
                is_visible = (pid in visible_pids)

                # Nur killen, wenn nicht sichtbar UND kein Butler-Audio-Prozess
                if not is_shell_main and not is_visible:
                    print(f"Banne Geist: {name} (PID {pid})")
                    proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

if __name__ == "__main__":
    print("Exorzismus-Protokoll aktiv (Butler-Safe-Mode).")
    while True:
        perform_exorcism()
        time.sleep(10)


