from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 5 or "[GROK EMPFANGEN]" in text:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    
    # --- UPGRADE: BREITBILD & KOMPAKTHEIT (Identisch zu Meta) ---
    MAX_UI_WIDTH = 86 
    
    # Schriftfarbe Weiss (Universums-Stil) - text.strip() hinzugefügt
    styled_text = Text(text.strip(), style="bright_white", overflow="fold")
    
    panel = Panel( # .fit entfernt für stabile Breite
        styled_text,
        # Titel in Gelb (Identisch zum Butler/Nervensystem)
        title=f"[bold #FFEE00]GROK @ {zeit}[/bold #FFEE00]",
        border_style="#FFEE00", # Gelber Rahmen
        subtitle="[dim white]xAI_Nexus_v1[/dim white]",
        padding=(0, 2), # Vertikales Padding auf 0
        width=MAX_UI_WIDTH,
        expand=False
    )
    
    # console.print("\n") # Gelöscht für lückenlosen Flow
    console.print(panel)


