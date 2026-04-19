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
 [bold #0084FF]     __  __  _____  ____   _      [/bold #0084FF]
 [bold #007BFF]    |  \\/  || ____||_  _| / \\     [/bold #007BFF]
 [bold #0072FF]    | |\\/| ||  _|    ||  / _ \\    [/bold #0072FF]
 [bold #0069FF]    | |  | || |___   || / ___ \\   [/bold #0069FF]
 [bold #0060FF]    |_|  |_||_____|  ||/_/   \\_\\  [/bold #0060FF]
 [bold #3b5998]     M E S S E N G E R  S Y N C   [/bold #3b5998]
"""

    console.print(vortex)
    console.print(Panel("[bold magenta]META_NEXUS_CORE: ONLINE (8002)[/bold magenta]", border_style="magenta", expand=False))
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

@app.post("/") 
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    sender_name = data.get("sender", "META") # <-- Den Namen fangen!
    
    if not raw_text: return {"status": "empty"}
    
    for p in plugins:
        try: 
            # Wir versuchen den Namen zu übergeben, falls das Plugin es kann
            p(raw_text, sender_name) 
        except TypeError:
            # Fallback für alte Plugins, die nur 'text' akzeptieren
            p(raw_text)
        except Exception as e: print(f"Meta-Plugin-Fehler: {e}")
    return {"status": "ok"}


if __name__ == "__main__":
    print_meta_banner()
    load_plugins()
    # Zündung auf Port 8002
    uvicorn.run(app, host="127.0.0.1", port=8002, log_level="error")
