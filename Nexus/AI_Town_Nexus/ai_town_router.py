import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib, pkgutil, os, uvicorn, re, threading, time
import pygetwindow as gw
import ctypes
from rich.console import Console
from rich.panel import Panel

# --- SYSTEM IDENTITÄT (Springer-Slot auf Port 8008) ---
PORT = 8008
TITLE = "AI_TOWN_NEXUS"
X_POS, Y_POS = 3185, 540  # Verankerung im Springer-Slot auf Monitor 2
WIDTH, HEIGHT = 625, 548  # Symmetrische Cockpit-Abmessungen

os.system(f"title {TITLE}")

# --- AUTOMATISCHER WINDOW-ANCHOR ---
def move_to_layout():
    time.sleep(1.0) # Kurzer Puffer, bis die Windows-Konsole den Titel gefressen hat
    try:
        wins = gw.getWindowsWithTitle(TITLE)
        if wins:
            win = wins[0]
            win.restore()
            win.moveTo(X_POS, Y_POS)
            win.resizeTo(WIDTH, HEIGHT)
            # Fixiert das Fenster im Cockpit-Raster gegen Überlappungs-Flimmern
            ctypes.windll.user32.SetWindowPos(win._hWnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    except: pass

def print_ai_town_banner():
    console = Console()
    # Deine präzise ausgerichtete Häuserzeile für Enjoy AI Town - Symmetrische Konturen bleiben unberührt!
    town_ascii = r"""
 [bold #00FF00]     ┌─────────┐   ┌─────────┐   ┌─────────┐     [/bold #00FF00]
 [bold #00FF00]    /  ▲ ▲ ▲  / \ /  ▲ ▲ ▲  / \ /  ▲ ▲ ▲  / \    [/bold #00FF00]
 [bold #00CC00]   █─────────█───█─────────█───█─────────█   [/bold #00CC00]
 [bold #009900]   │  █   █  │   │  █   █  │   │  █   █  │   [/bold #009900]
 [bold #006600]   │  █ ▀ █  │ ▄ │  █ ▀ █  │ ▄ │  █ ▀ █  │   [/bold #006600]
 [bold #004400]   └──▀───▀──┴───┴──▀───▀──┴───┴──▀───▀──┘   [/bold #004400]
 [bold #00FF00]   ┌────────────────────────────────────────┐   [/bold #00FF00]
 [bold #00CC00]   │ ─── WELCOME TO ENJOY AI TOWN CORE ───  │   [/bold #00CC00]
 [bold #004400]   └────────────────────────────────────────┘   [/bold #004400]
"""
    console.print(town_ascii)
    
    # Das konsistente AI-Town Panel auf Port 8008
    console.print(Panel(
        "[bold white]AI_TOWN_NEXUS: ONLINE (Port 8008)[/bold white]", 
        subtitle="[bold #00FF00]Enjoy AI Town Ecosystem[/bold #00FF00]",
        border_style="#00FF00", 
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

plugins = []

def load_plugins():
    global plugins
    plugins = []
    # Sucht die Plugins spezifisch im Unterordner von AI Town
    path = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.exists(path):
        os.makedirs(path)
    for loader, name, is_pkg in pkgutil.iter_modules([path]):
        try:
            module = importlib.import_module(f'plugins.{name}')
            importlib.reload(module)
            if hasattr(module, 'run'):
                plugins.append(module.run)
                print(f"    -> AI-Town-Platte geladen: {name}")
        except Exception as e:
            print(f"    [!] Fehler bei {name}: {e}")

@app.post("/webhook")
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    for p in plugins:
        try: p(raw_text) 
        except Exception as e: print(f"AI-Town-Nexus-Fehler: {e}")
    return {"status": "ok"}

if __name__ == "__main__":
    print_ai_town_banner()
    load_plugins()
    # Zündet den parallelen Thread für das automatische Einrasten im Cockpit
    threading.Thread(target=move_to_layout, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="error")

