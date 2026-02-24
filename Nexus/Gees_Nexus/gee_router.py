import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib
import pkgutil
import os
import uvicorn
import re
import threading
from rich.console import Console
from rich.panel import Panel

# --- BANNER ---
def print_andross_banner():
    console = Console()
    andross = """
      [bold red]      ▄▄▄████████▄▄▄      [/bold red]
      [bold red]    ▄██▀▀        ▀▀██▄    [/bold red]
      [bold red]  ▄██▀              ▀██▄  [/bold red]
      [bold red] █▀ [bold white]██[/bold white]            [bold white]██[/bold white] ▀█ [/bold red]
      [bold red] █  [bold white]██[/bold white]    [bold red]▄▄▄▄[/bold red]    [bold white]██[/bold white]  █ [/bold red]
      [bold red] █      [bold red]█▀  ▀█[/bold red]      █ [/bold red]
      [bold red] ▀██▄    [bold red]▀▀▀▀[/bold red]    ▄██▀  [/bold red]
      [bold red]   ▀████▄▄▄▄▄▄████▀    [/bold red]
    """
    console.print(andross)
    console.print(Panel("[bold green]GEE_NEXUS_ONLINE: READY[/bold green]", border_style="red", expand=False))

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
                print(f"    -> Platte geladen: {name}")
        except Exception as e:
            print(f"    [!] Fehler bei {name}: {e}")

@app.post("/webhook")
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    for p in plugins:
        try: p(raw_text) # Zurück zum synchronen Original
        except Exception as e: print(f"Plugin-Fehler: {e}")
    return {"status": "ok"}


if __name__ == "__main__":
    print_andross_banner()
    load_plugins()
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")

