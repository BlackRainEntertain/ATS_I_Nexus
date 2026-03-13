import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib, pkgutil, os, uvicorn
from rich.console import Console
from rich.panel import Panel

def print_gpt_banner():
    console = Console()
    gpt_logo = r"""
 [bold #00A67E]  █████████   █████████   █████████ [/bold #00A67E]
 [bold #00A67E]  ██          ██     ██      ██    [/bold #00A67E]
 [bold #008968]  ██   █████  █████████      ██    [/bold #008968]
 [bold #008968]  ██      ██  ██             ██    [/bold #008968]
 [bold #006B51]  █████████   ██             ██    [/bold #006B51]
 [bold #006B51]      ─── TRANSFORMER ───       [/bold #006B51]
"""
    console.print(gpt_logo)
    console.print(Panel("[bold white]GPT_NEXUS_CORE: ONLINE (Port 8003)[/bold white]", border_style="green", expand=False))
    
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
    path = os.path.join(os.path.dirname(__file__), 'plugins')
    if not os.path.exists(path): os.makedirs(path)
    for loader, name, is_pkg in pkgutil.iter_modules([path]):
        try:
            module = importlib.import_module(f'plugins.{name}')
            importlib.reload(module)
            if hasattr(module, 'run'):
                plugins.append(module.run)
                print(f"    -> GPT-Platte geladen: {name}")
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
    # Zündung auf Port 8003
    uvicorn.run(app, host="127.0.0.1", port=8003, log_level="error")


