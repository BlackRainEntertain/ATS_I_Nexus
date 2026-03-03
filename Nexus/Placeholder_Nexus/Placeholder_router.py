import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib
import pkgutil
import os
import uvicorn
from rich.console import Console
from rich.panel import Panel

# --- VEGA BANNER (Die violette Supernova) ---
def print_vega_banner():
    console = Console()
    # Das Symbol für Vega: Ein pulsierender Kern aus Empathie
    vega_eye = """
      [bold magenta]      .   [bold white]  *  [/bold white]   .      [/bold magenta]
      [bold magenta]    .  '  [bold white] / \ [/bold white]  '  .    [/bold magenta]
      [bold magenta]  .      [bold white]<  O  >[/bold white]      .  [/bold magenta]
      [bold magenta] .     [bold white]  \ / [/bold white]     . [/bold magenta]
      [bold magenta] .     [bold white]   *  [/bold white]     . [/bold magenta]
      [bold magenta]  .     [bold magenta]  140  [/bold magenta]    .  [/bold magenta]
      [bold magenta]    .      [bold white]RESONANZ[/bold white]   .    [/bold magenta]
      [bold magenta]      '  .  .  '      [/bold magenta]
    """
    console.print(vega_eye)
    console.print(Panel("[bold white]VEGA_NEXUS_VORTEX: ONLINE (Port 8003)[/bold white]", border_style="magenta", expand=False))

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

plugins = []

def load_plugins():
    global plugins
    plugins = []
    # Pfad zum Vega-plugins-Ordner
    path = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.exists(path):
        os.makedirs(path)
    for loader, name, is_pkg in pkgutil.iter_modules([path]):
        try:
            module = importlib.import_module(f'plugins.{name}')
            importlib.reload(module)
            if hasattr(module, 'run'):
                plugins.append(module.run)
                print(f"    -> Vega-Platte geladen: {name}")
        except Exception as e:
            print(f"    [!] Fehler bei Vega-Plugin {name}: {e}")

@app.post("/") # Der Affe schickt bei Vega auch an "/"
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    
    for p in plugins:
        try: p(raw_text) 
        except Exception as e: print(f"Vega-Plugin-Fehler: {e}")
    return {"status": "ok"}

if __name__ == "__main__":
    print_vega_banner()
    load_plugins()
    # Zündung auf Port 8003 für Vega
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")
