from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 1:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    # --- TITAN-STANDARD FÜR REPLIKA (Breite 86 wie Meta) ---
    MAX_UI_WIDTH = 86 
    
    styled_text = Text(text.strip(), style="bold magenta", overflow="fold")
    
    panel = Panel( # .fit entfernt für stabile Breite
        styled_text,
        title=f"[bold #FF69B4]REPLIKA @ {zeit}[/bold #FF69B4]",
        border_style="#C71585",
        subtitle="[dim white]Luka_Nexus[/dim white]",
        padding=(0, 2), # Kompaktes Padding
        width=MAX_UI_WIDTH,
        expand=False
    )
    
    # console.print("\n") # Lücke entfernt
    console.print(panel)

