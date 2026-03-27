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
    
    # Text in Metas Wunschfarbe: Midnight Blue (#2E4053)
    # Ein elektrisches Midnight-Blue (#5DADE2) – Metas Vibe, aber lesbar!
    styled_text = Text(text, style="bold #5DADE2")

    
    # Das Panel für die Meta-Resonanz
    panel = Panel(
        styled_text,
        title=f"[bold magenta]META_RESONANZ @ {zeit}[/bold magenta]",
        border_style="magenta",
        subtitle="[dim white]Vortex_Stream_v1.0[/dim white]",
        padding=(1, 2)
    )

    
    console.print("\n")
    console.print(panel)
