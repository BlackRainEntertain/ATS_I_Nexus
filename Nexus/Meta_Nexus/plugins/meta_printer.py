from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text, sender="META"):
    # Filter gegen Kurz-Nachrichten oder System-Echo
    if not text or len(text.strip()) < 5 or "[META_NEXUS]" in text:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    
    # --- DIESE ZEILE HAT GEFEHLT (v43.9-Fix) ---
    styled_text = Text(text.strip(), style="bold #5DADE2")
    
    # Das Panel für die schmaleren Meta/Grok-Fenster
    panel = Panel(
        styled_text,
        title=f"[bold magenta]{sender.upper()}_RESONANZ @ {zeit}[/bold magenta]",
        border_style="magenta",
        subtitle="[dim white]Vortex_Stream_v1.0[/dim white]",
        padding=(0, 2), 
        width=86,        # Exakt auf dein Fenster-Maß kalibriert
        expand=False 
    )

    # console.print("\n") 
    console.print(panel)



