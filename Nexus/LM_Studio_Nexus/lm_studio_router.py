import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib, pkgutil, os, uvicorn, re, threading, time
import json
import pygetwindow as gw
import ctypes
import httpx
from rich.console import Console
from rich.panel import Panel

# Pfad zu deinem echten LM-Studio Konversations-Archiv
CONV_DIR = r"C:\Users\René\.lmstudio\conversations"
# Ziel-Mündung für dein zentrales Butler-System (Port 8007 Webhook!)
VOICE_ENDPOINT = "http://127.0.0.1:8007/webhook"

last_seen_texts = {}

# --- COCKPIT SNAP LOGIK ---
def snap_to_grid():
    time.sleep(2.0)
    title_part = "LM_STUDIO_NEXUS"
    OFFSET_X = 2560
    X, Y, W, H = OFFSET_X + 625, 540, 625, 548
    windows = [w for w in gw.getWindowsWithTitle('') if title_part in w.title.upper()]
    if windows:
        win = windows[0]
        try:
            win.restore()
            win.moveTo(X, Y)
            win.resizeTo(W, H)
            ctypes.windll.user32.SetWindowPos(win._hWnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
        except Exception as e: pass

def print_lm_studio_banner():
    os.system("title LM_STUDIO_NEXUS")
    console = Console()
    lm_core = r"""
 [bold #FF8C00]     ▄▄████████▄▄      ▄▄████████▄▄    [/bold #FF8C00]
 [bold #FF4500]    ███▀    ▀████    ████▀    ▀███   [/bold #FF4500]
 [bold #FF4500]    ██   [bold #FFFF00]▄██▄[/bold #FFFF00]  ██████████  [bold #FFFF00]▄██▄[/bold #FFFF00]   ██   [/bold #FF4500]
 [bold #FF4500]    ▀██▄ [bold #FFFF00]▀██▀[/bold #FFFF00]  ▀▀▀[bold #FFA500][ LM ][/bold #FFA500]▀▀▀  [bold #FFFF00]▀██▀[/bold #FFFF00] ▄██▀   [/bold #FF4500]
 [bold #990000]      ▀██████▀▀   ▀▀   ▀▀██████▀     [/bold #990000]
 [bold #660000]                ▀▀▀▀                 [/bold #660000]
 [bold #330000] ─── LM Studio Universal Engine // Port 8007 ─── [/bold #330000]
"""
    console.print(lm_core)
    console.print(Panel(
        "[bold white]LM_NEXUS_CORE: ONLINE (Frequenz-Kanal 8007)[/bold white]", 
        subtitle="[bold #FF4500]Pure Archive Sync Modus[/bold #FF4500]", 
        border_style="#FF4500", 
        expand=False
    ))

    # --- DAS INTERAKTIVE HUD (v42.2) ---
    console.print("\n [bold cyan]NEXUS LARYNX PROTOKOLL:[/bold cyan]")
    console.print(" [white]Diktat:[/white] [bold green]Texteingabe[/bold green] ➔ [bold red]Abbruch[/bold red] ➔ [bold yellow]Nexus Fertig[/bold yellow] ➔ [bold blue]Absenden[/bold blue]")
    console.print(" [white]Audio: [/white] [bold dim]Pause, Weiter, Skip, Stopp[/bold dim]")
    console.print(" [white]Nexus: [/white] [bold green]Hey Gee, Guten Morgen[/bold green] [white]/[/white] [bold red]Feierabend, Shutdown[/bold red]")
    console.print(" [white]System:[/white] [bold #FF4500]PC VOLLSTÄNDIG HERUNTERFAHREN[/bold #FF4500] ➔ [italic]Ich Liebe Sara[/italic] [dim](oder Abschaltprotokoll)[/dim]")
    console.print(" [dim]─────────────────────────────────────────────────────────────[/dim]\n")

def extract_last_assistant_text(file_path):
    """Extrahiert blitzschnell die allerletzte KI-Antwort aus der LM-Studio JSON"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            messages = data.get("messages", [])
            if not messages: return None
            
            for msg in reversed(messages):
                versions = msg.get("versions", [])
                if versions and msg.get("currentlySelected") is not None:
                    idx = msg.get("currentlySelected")
                    v = versions[idx]
                    if v.get("role") == "assistant":
                        text_parts = []
                        for c in v.get("content", []):
                            if c.get("type") == "text": text_parts.append(c.get("text", ""))
                        if not text_parts and v.get("steps"):
                            for step in v.get("steps"):
                                for c in step.get("content", []):
                                    if c.get("type") == "text": text_parts.append(c.get("text", ""))
                        return "".join(text_parts).strip()
    except: pass
    return None

def archive_watchdog():
    """Überwacht das Archiv im lautlosen Jitter-Takt (0.0% CPU-Last beim Zocken)"""
    print("[*] Archiv-Wächter AKTIV. Lausche stur auf deine LM-Studio Chats...")
    while True:
        time.sleep(1.0)
        if not os.path.exists(CONV_DIR): continue
        try:
            for file in os.listdir(CONV_DIR):
                if file.endswith(".json"):
                    full_path = os.path.join(CONV_DIR, file)
                    if (time.time() - os.path.getmtime(full_path)) < 2.0:
                        last_text = extract_last_assistant_text(full_path)
                        if last_text and len(last_text) > 2:
                            if last_seen_texts.get(file) != last_text:
                                last_seen_texts[file] = last_text
                                print(f"[+] Neue Nachricht im Archiv erkannt ➔ Sende Ticket an Webhook.")
                                try: httpx.post(VOICE_ENDPOINT, json={"text": last_text}, timeout=5.0)
                                except: pass
        except: pass

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
                print(f"    -> LM-Studio-Platte geladen: {name}")
        except Exception as e:
            print(f"    [!] Fehler bei {name}: {e}")

@app.post("/webhook")
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    for p in plugins:
        try: p(raw_text) 
        except Exception as e: print(f"LM-Studio-Nexus-Fehler: {e}")
    return {"status": "ok"}

if __name__ == "__main__":
    print_lm_studio_banner()
    load_plugins()
    # Zünde die beiden Hintergrund-Antriebe (Snap & Watchdog) parallel im RAM!
    threading.Thread(target=snap_to_grid, daemon=True).start()
    threading.Thread(target=archive_watchdog, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8007, log_level="error")
