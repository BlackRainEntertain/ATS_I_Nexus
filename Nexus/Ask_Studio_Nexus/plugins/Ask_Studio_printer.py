from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 1:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    # --- TITAN-STANDARD FÜR STUDIO (Breite 95 wie Gee/Atsi) ---
    MAX_UI_WIDTH = 95 
    
    # Text in hellem Weiß für maximalen Kontrast auf dunklem Grund
    styled_text = Text(text.strip(), style="bold white", overflow="fold")
    
    panel = Panel( # .fit entfernt für stabile Breite
        styled_text,
        title=f"[bold #FF0000]STUDIO_PARTNER @ {zeit}[/bold #FF0000]",
        border_style="#FF0000",
        subtitle="[bold #282828]Creative_Nexus[/bold #282828]",
        padding=(0, 2), # Vertikales Padding auf 0
        width=MAX_UI_WIDTH,
        expand=False
    )
    
    # console.print("\n") # Lücke entfernt
    console.print(panel)

