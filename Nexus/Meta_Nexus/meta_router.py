import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib
import pkgutil
import os
import uvicorn
from rich.console import Console
from rich.panel import Panel

# --- META BANNER (Der Vortex) ---
def print_meta_banner():
    console = Console()
    # Ein stilisierter Wirbel/Vortex für Meta
    vortex = """
      [bold magenta]      .        .      [/bold magenta]
      [bold magenta]    .  '      '  .    [/bold magenta]
      [bold magenta]  .      [bold white]████[/bold white]      .  [/bold magenta]
      [bold magenta] .     [bold white]█▀    ▀█[/bold white]     . [/bold magenta]
      [bold magenta] .     [bold white]█      █[/bold white]     . [/bold magenta]
      [bold magenta]  .     [bold white]█▄    ▄█[/bold white]    .  [/bold magenta]
      [bold magenta]    .      [bold white]▀▀▀▀[/bold white]   .    [/bold magenta]
      [bold magenta]      '  .  .  '      [/bold magenta]
    """
    console.print(vortex)
    console.print(Panel("[bold magenta]META_NEXUS_VORTEX: READY[/bold magenta]", border_style="magenta", expand=False))

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

plugins = []

def load_plugins():
    global plugins
    plugins = []
    # Pfad zum lokalen plugins-ordner in Nexus/Meta_Nexus
    path = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.exists(path):
        os.makedirs(path)
    for loader, name, is_pkg in pkgutil.iter_modules([path]):
        try:
            # Dynamisches Importieren der Meta-Platten
            module = importlib.import_module(f'plugins.{name}')
            importlib.reload(module)
            if hasattr(module, 'run'):
                plugins.append(module.run)
                print(f"    -> Meta-Platte geladen: {name}")
        except Exception as e:
            print(f"    [!] Fehler bei Meta-Plugin {name}: {e}")

@app.post("/") # Der Affe schickt an "/"
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    
    # Jage den Text durch alle geladenen Meta-Plugins
    for p in plugins:
        try: p(raw_text) 
        except Exception as e: print(f"Meta-Plugin-Fehler: {e}")
    return {"status": "ok"}

if __name__ == "__main__":
    print_meta_banner()
    load_plugins()
    # Zündung auf Port 8002
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="error")
