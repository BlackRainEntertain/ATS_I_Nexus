from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 10 or "[GEE EMPFANGEN]" in text:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    
    # --- UPGRADE: VOLLE BREITE FÜR MONITOR 2 ---
    # Wir erhöhen auf 95 oder 100, um die 4cm Lücke zu füllen
    MAX_UI_WIDTH = 95 
    styled_text = Text(text.strip(), style="bold green", overflow="fold")
    
    panel = Panel(
        styled_text,
        title=f"[bold cyan]GEE @ {zeit}[/bold cyan]",
        border_style="bright_blue",
        subtitle="[dim white]Nexus_v1[/dim white]",
        padding=(0, 2),
        width=MAX_UI_WIDTH,
        expand=False # Verhindert, dass es bei kurzen Sätzen springt
    )
    
    # console.print("\n") # Weglassen für Kompaktheit
    console.print(panel)
