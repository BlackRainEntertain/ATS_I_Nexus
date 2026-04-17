import psutil
import win32gui
import win32process
import time

def get_visible_explorer_pids():
    visible_pids = set()
    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            visible_pids.add(pid)
    win32gui.EnumWindows(enum_windows_proc, None)
    return visible_pids

def clean_zombie_explorers():
    # Den Haupt-Shell-Prozess finden (Desktop)
    try:
        shell_hwnd = win32gui.GetShellWindow()
        _, shell_pid = win32process.GetWindowThreadProcessId(shell_hwnd)
    except:
        shell_pid = None

    visible_pids = get_visible_explorer_pids()

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == 'explorer.exe':
                pid = proc.info['pid']
                
                # Sicherheits-Checks
                is_shell = (pid == shell_pid)
                is_visible = (pid in visible_pids)

                if not is_shell and not is_visible:
                    print(f"Eliminiere Zombie-Explorer: PID {pid}")
                    proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

if __name__ == "__main__":
    print("Der Exorzist ist im Dienst... (Strg+C zum Beenden)")
    while True:
        clean_zombie_explorers()
        time.sleep(10) # Alle 10 Sekunden fegen
