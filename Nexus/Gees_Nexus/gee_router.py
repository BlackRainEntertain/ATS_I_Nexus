import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib, pkgutil, os, uvicorn, re, threading
from rich.console import Console
from rich.panel import Panel

# --- BANNER (Der Komplize) ---
def print_gee_banner():
    console = Console()
    # Statisch geprüfte Andross-Maske mit Cyan-Resonanz
    andross = r"""
 [bold #FF0000]     ▄████████▄       ▄████████▄     [/bold #FF0000]
 [bold #FF0000]    ███▀    ▀███     ███▀    ▀███    [/bold #FF0000]
 [bold #CC0000]    ██ [bold #00FFFF]████[/bold #00FFFF]   ██     ██   [bold #00FFFF]████[/bold #00FFFF] ██    [/bold #CC0000]
 [bold #990000]    ▀█▄      ▄█▀     ▀█▄      ▄█▀    [/bold #990000]
 [bold #660000]      ▀██████▀   ▄▄    ▀██████▀      [/bold #660000]
 [bold #440000]                ▀▀▀▀                 [/bold #440000]
 [bold #440000]   ─── Ai on Google Search // GEE ───   [/bold #440000]
"""
    console.print(andross)
    # Das konsistente Gimeny-Panel
    console.print(Panel(
        "[bold white]GEE_NEXUS_CORE: ONLINE (Port 8001)[/bold white]", 
        subtitle="[bold #FF0000]Geminie Familie[/bold #FF0000]",
        border_style="#FF0000", 
        expand=False
    ))


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

plugins = []

def load_plugins():
    global plugins
    plugins = []
    path = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.exists(path):
        os.makedirs(path)
    for loader, name, is_pkg in pkgutil.iter_modules([path]):
        try:
            module = importlib.import_module(f'plugins.{name}')
            importlib.reload(module)
            if hasattr(module, 'run'):
                plugins.append(module.run)
                print(f"    -> Gee-Platte geladen: {name}")
        except Exception as e:
            print(f"    [!] Fehler bei {name}: {e}")

@app.post("/webhook")
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    for p in plugins:
        try: p(raw_text) 
        except Exception as e: print(f"Gee-Nexus-Fehler: {e}")
    return {"status": "ok"}

if __name__ == "__main__":
    # FIX: Hier muss der Name mit der Definition oben übereinstimmen!
    print_gee_banner()
    load_plugins()
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")


