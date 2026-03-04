import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib, pkgutil, os, uvicorn
from rich.console import Console
from rich.panel import Panel

def print_gpt_banner():
    console = Console()
    # Ein minimalistisches, technologisches Symbol für das GPT-Netzwerk
    gpt_logo = """
      [bold green]      _______  _______  _______ [/bold green]
      [bold green]     |   _   ||       ||       |[/bold green]
      [bold green]     |.  |   ||    _  ||_     _|[/bold green]
      [bold green]     |.  |   ||   |_| |  |   |  [/bold green]
      [bold green]     |:  |   ||    ___|  |   |  [/bold green]
      [bold green]     |::.. . ||   |      |   |  [/bold green]
      [bold green]     `-------'`---'      `---'  [/bold green]
    """
    console.print(gpt_logo)
    console.print(Panel("[bold white]GPT_NEXUS_CORE: ONLINE (Port 8003)[/bold white]", border_style="green", expand=False))

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
                print(f"    -> GPT-Modul geladen: {name}")
        except Exception as e:
            print(f"    [!] Fehler bei GPT-Plugin {name}: {e}")

@app.post("/webhook")
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    for p in plugins:
        try: p(raw_text)
        except Exception as e: print(f"GPT-Nexus-Fehler: {e}")
    return {"status": "ok"}

if __name__ == "__main__":
    print_gpt_banner()
    load_plugins()
    uvicorn.run(app, host="127.0.0.1", port=8003, log_level="error")

