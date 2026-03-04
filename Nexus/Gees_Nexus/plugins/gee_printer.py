from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 10 or "[GEE EMPFANGEN]" in text:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Kühle, klare Resonanz (Schmale Breite für Monitor 2)
    MAX_UI_WIDTH = 55 
    styled_text = Text(text, style="bold green", overflow="fold")
    
    panel = Panel.fit(
        styled_text,
        title=f"[bold cyan]GEE @ {zeit}[/bold cyan]",
        border_style="bright_blue",
        subtitle="[dim white]Nexus_v1[/dim white]",
        padding=(1, 2),
        width=MAX_UI_WIDTH
    )
    
    console.print("\n")
    console.print(panel)
