from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    # Filter gegen Kurz-Nachrichten oder System-Echo
    if not text or len(text.strip()) < 5 or "[META_NEXUS]" in text:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Text in fettem Magenta (Llama-Style)
    styled_text = Text(text, style="bold magenta")
    
    # Das Panel für die Meta-Resonanz
    panel = Panel(
        styled_text,
        title=f"[bold lila]META_RESONANZ @ {zeit}[/bold lila]",
        border_style="magenta",
        subtitle="[dim white]Vortex_Stream_v1.0[/dim white]",
        padding=(1, 2)
    )
    
    console.print("\n")
    console.print(panel)
