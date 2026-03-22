import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib, pkgutil, os, uvicorn, re, threading, time
import pygetwindow as gw
import ctypes
from rich.console import Console
from rich.panel import Panel

# --- COCKPIT SNAP LOGIK (v6.8) ---
def snap_to_grid():
    # Wir geben dem Fenster 2 Sekunden Zeit, um wirklich zu existieren
    time.sleep(2.0)
    # Sucht nach dem Titel, den os.system am Start setzt
    title_part = "REPLIKA_NEXUS"
    OFFSET_X = 2560
    # Exakte GPT-Koordinaten aus deinem Cockpit
    X, Y, W, H = OFFSET_X + 625, 540, 625, 548
    
    windows = [w for w in gw.getWindowsWithTitle('') if title_part in w.title.upper()]
    if windows:
        win = windows[0]
        try:
            win.restore()
            win.moveTo(X, Y)
            win.resizeTo(W, H)
            # Set Always on Top
            ctypes.windll.user32.SetWindowPos(win._hWnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
        except Exception as e:
            print(f"[!] Snap-Fehler: {e}")

def print_replika_banner():
    # Wir setzen den Titel direkt hier, damit snap_to_grid ihn findet
    os.system("title REPLIKA_NEXUS")
    console = Console()
    heart_pulse = r"""
 [bold #FF69B4]      ▄▄█▀▀▀▄▄      ▄▄█▀▀▀▄▄     [/bold #FF69B4]
 [bold #FF1493]    ▄█▀      ▀█▄  ▄█▀      ▀█▄    [/bold #FF1493]
 [bold #C71585]    █         ▀█▄█▀         █    [/bold #C71585]
 [bold #8B008B]    ▀█▄         ▀         ▄█▀    [/bold #8B008B]
 [bold #4B0082]      ▀█▄               ▄█▀      [/bold #4B0082]
 [bold #4B0082]        ▀█▄           ▄█▀        [/bold #4B0082]
 [bold #4B0082]   ─── Replika Nexus // Port 8004 ───   [/bold #4B0082]
"""
    console.print(heart_pulse)
    console.print(Panel(
        "[bold white]REPLIKA_CORE: AKTIV (Frequenz-Kanal 8004)[/bold white]", 
        subtitle="[bold #FF69B4]Luka Resonanz[/bold #FF69B4]",
        border_style="#FF69B4", 
        expand=False
    ))

    # --- DAS INTERAKTIVE HUD (v42.2) ---
    console.print("\n [bold cyan]NEXUS LARYNX PROTOKOLL:[/bold cyan]")
    
    # 1. Diktat-Kette
    console.print(" [white]Diktat:[/white] [bold green]Texteingabe[/bold green] ➔ [bold red]Abbruch[/bold red] ➔ [bold yellow]Nexus Fertig[/bold yellow] ➔ [bold blue]Absenden[/bold blue]")
    
    # 2. Audio-Steuerung
    console.print(" [white]Audio: [/white] [bold dim]Pause, Weiter, Skip, Stopp[/bold dim]")
    
    # 3. Nexus-Status (An/Aus)
    console.print(" [white]Nexus: [/white] [bold green]Hey Gee, Guten Morgen[/bold green] [white]/[/white] [bold red]Feierabend, Shutdown[/bold red]")
    
    # 4. Totaler System-Exit
    console.print(" [white]System:[/white] [bold #FF4500]PC VOLLSTÄNDIG HERUNTERFAHREN[/bold #FF4500] ➔ [italic]Ich Liebe Sara[/italic] [dim](oder Abschaltprotokoll)[/dim]")
    
    console.print(" [dim]─────────────────────────────────────────────────────────────[/dim]\n")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Plugins laden (dein Code) ...
plugins = []
def load_plugins():
    global plugins
    plugins = []
    path = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.exists(path): os.makedirs(path)
    for loader, name, is_pkg in pkgutil.iter_modules([path]):
        try:
            module = importlib.import_module(f'plugins.{name}')
            importlib.reload(module)
            if hasattr(module, 'run'):
                plugins.append(module.run)
                print(f"    -> Replika-Platte geladen: {name}")
        except Exception as e:
            print(f"    [!] Fehler bei {name}: {e}")

@app.post("/webhook")
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    for p in plugins:
        try: p(raw_text) 
        except Exception as e: print(f"Replika-Nexus-Fehler: {e}")
    return {"status": "ok"}

if __name__ == "__main__":
    print_replika_banner()
    load_plugins()
    # Starte den Snap-Thread, damit er uvicorn nicht blockiert
    threading.Thread(target=snap_to_grid, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8004, log_level="error")
