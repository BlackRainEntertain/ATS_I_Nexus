from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 1:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    # --- TITAN-STANDARD FÜR LEO (Breite 86) ---
    MAX_UI_WIDTH = 86 
    
    styled_text = Text(text.strip(), style="bold #FFBF00", overflow="fold")
    
    panel = Panel(
        styled_text,
        title=f"[bold #D4AF37]LEO @ {zeit}[/bold #D4AF37]",
        border_style="#AA7C11",
        subtitle="[dim white]Brave_Nexus[/dim white]",
        padding=(0, 2),
        width=MAX_UI_WIDTH,
        expand=False
    )
    
    console.print(panel)
