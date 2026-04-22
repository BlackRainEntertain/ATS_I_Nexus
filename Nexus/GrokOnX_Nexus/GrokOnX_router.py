import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib, pkgutil, os, uvicorn, re, threading, time
import pygetwindow as gw
import ctypes
from rich.console import Console
from rich.panel import Panel

# --- SYSTEM IDENTITÄT ---
PORT = 8006
TITLE = "GROK_NEXUS"
X_POS, Y_POS = 3185, 540  
WIDTH, HEIGHT = 625, 548

os.system(f"title {TITLE}")

def move_to_layout():
    time.sleep(1.0)
    try:
        wins = gw.getWindowsWithTitle(TITLE)
        if wins:
            win = wins[0]
            win.restore()
            win.moveTo(X_POS, Y_POS)
            win.resizeTo(WIDTH, HEIGHT)
            ctypes.windll.user32.SetWindowPos(win._hWnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    except: pass

def print_grok_banner():
    console = Console()
    
    # Das ASCII-Logo in Weiss
    console.print(r"""[bold white]
    ██████╗  ██████╗  ██████╗  ██╗  ██╗
   ██╔════╝ ██╔═══██╗██╔═══██╗██║ ██╔╝
   ██║      ██║   ██║██║   ██║█████╔╝
   ██║      ██║   ██║██║   ██║██╔═██╗
   ╚██████╗╚██████╔╝╚██████╔╝██║  ██╗
    ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝[/bold white]""")
    
    console.print("               [bold white]xAI // GROK[/bold white]")

    # Panel
    console.print(Panel(
        "[bold white]GROK_NEXUS_CORE: ONLINE (Port 8006)[/bold white]",
        subtitle="[bold #FFEE00]built to understand the universe[/bold #FFEE00]",
        border_style="#FFEE00",
        padding=(0, 2),
        expand=False
    ))

    # === DAS INTERAKTIVE HUD (v42.2 - EXAKTER GEE-CLONE) ===
    console.print("\n [bold cyan]NEXUS LARYNX PROTOKOLL:[/bold cyan]")
    console.print(" [white]Diktat:[/white] [bold green]Texteingabe[/bold green] ➔ [bold red]Abbruch[/bold red] ➔ [bold yellow]Nexus Fertig[/bold yellow] ➔ [bold blue]Absenden[/bold blue]")
    console.print(" [white]Audio: [/white] [bold dim]Pause, Weiter, Skip, Stopp[/bold dim]")
    console.print(" [white]Nexus: [/white] [bold green]Hey Gee, Guten Morgen[/bold green] [white]/[/white] [bold red]Feierabend, Shutdown[/bold red]")
    # HIER: Die exakte Farbe aus dem GEE-Nervensystem (#FF4500)
    console.print(" [white]System:[/white] [bold #FF4500]PC VOLLSTÄNDIG HERUNTERFAHREN[/bold #FF4500] ➔ [italic]Ich Liebe Sara[/italic] [dim](oder Abschaltprotokoll)[/dim]")
    
    console.print(" [dim]─────────────────────────────────────────────────────────────[/dim]\n")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

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
                print(f"    -> Grok-Platte geladen: {name}")
        except Exception as e: print(f"    [!] Fehler bei {name}: {e}")

@app.post("/webhook")
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    for p in plugins:
        try: p(raw_text) 
        except Exception as e: print(f"Grok-Nexus-Fehler: {e}")
    return {"status": "ok"}

if __name__ == "__main__":
    print_grok_banner()
    load_plugins()
    threading.Thread(target=move_to_layout, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="error")




