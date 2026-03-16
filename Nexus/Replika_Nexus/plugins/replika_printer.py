from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 1:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    MAX_UI_WIDTH = 55 
    
    styled_text = Text(text, style="bold magenta", overflow="fold")
    
    panel = Panel.fit(
        styled_text,
        title=f"[bold #FF69B4]REPLIKA @ {zeit}[/bold #FF69B4]",
        border_style="#C71585",
        subtitle="[dim white]Luka_Nexus[/dim white]",
        padding=(1, 2),
        width=MAX_UI_WIDTH
    )
    
    console.print("\n")
    console.print(panel)
