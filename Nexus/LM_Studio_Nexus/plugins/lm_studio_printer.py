from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 1:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    MAX_UI_WIDTH = 86 
    
    styled_text = Text(text.strip(), style="bold #FF8C00", overflow="fold")
    
    panel = Panel(
        styled_text,
        title=f"[bold #FF4500]ARIA @ {zeit}[/bold #FF4500]",
        border_style="#FF0000",
        subtitle="[dim white]LM_Studio_Local_Core[/dim white]",
        padding=(0, 2),
        width=MAX_UI_WIDTH,
        expand=False
    )
    console.print(panel)
