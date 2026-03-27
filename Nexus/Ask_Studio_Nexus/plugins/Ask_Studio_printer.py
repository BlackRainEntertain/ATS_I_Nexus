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
    
    # Text in hellem Weiß für maximalen Kontrast auf dunklem Grund
    styled_text = Text(text, style="bold white", overflow="fold")
    
    panel = Panel.fit(
        styled_text,
        title=f"[bold #FF0000]STUDIO_PARTNER @ {zeit}[/bold #FF0000]",
        border_style="#FF0000",
        subtitle="[bold #282828]Creative_Nexus[/bold #282828]",
        padding=(1, 2),
        width=MAX_UI_WIDTH
    )
    
    console.print("\n")
    console.print(panel)
