import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib, pkgutil, os, uvicorn, re, threading, time
import json
import hashlib
import pygetwindow as gw
import ctypes
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# --- SYSTEM-PFADE (DEIN ABSOLUTES HARDWARE-GEFÜGE) ---
CONV_DIR = r"C:\Users\René\.lmstudio\conversations"
QUEUE_DIR = r"C:\Users\René\Desktop\LM Projekte\Nexus\Nexus\_Voice_Queue"

# Falls der Hauptpfad hakt, relativer Fallback
if not os.path.exists(QUEUE_DIR):
    QUEUE_DIR = r"C:\Users\René\Desktop\LM Projekte\Nexus\_Voice_Queue"

stabilization_cache = {}
last_sent_hashes = {}
console = Console()

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
    lm_core = r"""
 [bold #8A2BE2]      ▄▄          ▄▄      [/bold #8A2BE2]
 [bold #9400D3]    ▄████▄      ▄████▄    [/bold #9400D3]
 [bold #9400D3]    ██▄████████████▄██    [/bold #9400D3]
 [bold #BA55D3]    ███▀██████████▀███    [/bold #BA55D3]
 [bold #DA70D6]    ██████████████████    [/bold #DA70D6]
 [bold #DA70D6]      ▀██▀▀▀▀▀▀▀▀██▀      [/bold #DA70D6]
 [bold #8B008B]     ▄██  ▀▀  ▀▀  ██▄     [/bold #8B008B]
 [bold #4B0082] ─── LM Studio Space Invader Engine // Port 8007 ─── [/bold #4B0082]
"""
    console.print(lm_core)
    console.print(Panel(
        "[bold white]LM_NEXUS_CORE: ONLINE (Frequenz-Kanal 8007)[/bold white]", 
        subtitle="[bold #9400D3]Froggit Archive Sync[/bold #9400D3]", 
        border_style="#9400D3", 
        expand=False
    ))

    console.print("\n [bold cyan]NEXUS LARYNX PROTOKOLL:[/bold cyan]")
    console.print(" [white]Diktat:[/white] [bold green]Texteingabe[/bold green] ➔ [bold red]Abbruch[/bold red] ➔ [bold yellow]Nexus Fertig[/bold yellow] ➔ [bold blue]Absenden[/bold blue]")
    console.print(" [white]Audio: [/white] [bold dim]Pause, Weiter, Skip, Stopp[/bold dim]")
    console.print(" [white]Nexus: [/white] [bold green]Hey Gee, Guten Morgen[/bold green] [white]/[/white] [bold red]Feierabend, Shutdown[/bold red]")
    console.print(" [white]System:[/white] [bold #FF4500]PC VOLLSTÄNDIG HERUNTERFAHREN[/bold #FF4500] ➔ [italic]Ich Liebe Sara[/italic] [dim](oder Abschaltprotokoll)[/dim]")
    console.print(" [dim]─────────────────────────────────────────────────────────────[/dim]\n")

def extract_last_assistant_text(file_path):
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
    console.print("[bold #8B008B][*] Archiv-Wächter AKTIV. Lausche stur auf deine LM-Studio Chats...[/bold #8B008B]")
    while True:
        time.sleep(1.0)
        if not os.path.exists(CONV_DIR): continue
        try:
            for file in os.listdir(CONV_DIR):
                if file.endswith(".json"):
                    full_path = os.path.join(CONV_DIR, file)
                    
                    if (time.time() - os.path.getmtime(full_path)) < 30.0:
                        current_text = extract_last_assistant_text(full_path)
                        if not current_text or len(current_text) <= 5: continue
                        
                        state = stabilization_cache.get(file, {"text": "", "count": 0})
                        
                        if state["text"] == current_text:
                            state["count"] += 1
                        else:
                            state["text"] = current_text
                            state["count"] = 0
                            
                        stabilization_cache[file] = state
                        
                        # DER 5-SEKUNDEN-GOLDSTANDARD
                        if state["count"] >= 5:
                            current_hash = hashlib.md5(current_text.encode('utf-8')).hexdigest()
                            
                            if last_sent_hashes.get(file) != current_hash:
                                last_sent_hashes[file] = current_hash
                                
                                # Physisches JSON-Ticket generieren
                                ticket_data = {
                                    "owner": "LM_Studio",
                                    "voice": "de-DE-SeraphinaMultilingualNeural",
                                    "rate": "-4%",
                                    "pitch": "-2Hz",
                                    "text": current_text,
                                    "timestamp": time.time()
                                }
                                
                                if os.path.exists(QUEUE_DIR):
                                    ticket_file = os.path.join(QUEUE_DIR, f"ticket_lm_studio_{int(time.time())}.json")
                                    with open(ticket_file, "w", encoding="utf-8") as tf:
                                        json.dump(ticket_data, tf, ensure_ascii=False, indent=2)
                                    
                                    # --- DAS INTEGRATION-BOX-PROTOKOLL ---
                                    # Formatiert das lila Froggit-Interface live im CMD-Fenster!
                                    current_time = time.strftime("%H:%M:%S")
                                    panel_text = Text(current_text, style="#DA70D6")
                                    
                                    console.print(Panel(
                                        panel_text,
                                        title=f"[bold #BA55D3]LM_STUDIO @ {current_time}[/bold #BA55D3]",
                                        subtitle="[dim white]Nexus_v1[/dim white]",
                                        border_style="#9400D3",
                                        width=57,  # Perfekt zugeschnitten auf dein 625px-Fenster-Grid!
                                        expand=False
                                    ))
                                else:
                                    console.print(f"[bold red][!] FEHLER: _Voice_Queue nicht gefunden unter {QUEUE_DIR}[/bold red]")
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
                console.print(f"    [#DA70D6]-> LM-Studio-Platte geladen: {name}[/#DA70D6]")
        except: pass

@app.post("/webhook")
async def receive(request: Request):
    data = await request.json()
    raw_text = data.get("text", "").strip()
    if not raw_text: return {"status": "empty"}
    for p in plugins:
        try: p(raw_text) 
        except: pass
    return {"status": "ok"}

if __name__ == "__main__":
    print_lm_studio_banner()
    load_plugins()
    threading.Thread(target=snap_to_grid, daemon=True).start()
    threading.Thread(target=archive_watchdog, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8007, log_level="error")