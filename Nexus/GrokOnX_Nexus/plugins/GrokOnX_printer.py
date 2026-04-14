from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 5 or "[GROK EMPFANGEN]" in text:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    MAX_UI_WIDTH = 55 
    
    # Schriftfarbe Weiss (Universums-Stil)
    styled_text = Text(text, style="bright_white", overflow="fold")
    
    panel = Panel.fit(
        styled_text,
        # Titel in Gelb (Identisch zum Butler/Nervensystem)
        title=f"[bold #FFEE00]GROK @ {zeit}[/bold #FFEE00]",
        border_style="#FFEE00", # Gelber Rahmen
        subtitle="[dim white]xAI_Nexus_v1[/dim white]",
        padding=(1, 2),
        width=MAX_UI_WIDTH
    )
    
    console.print("\n")
    console.print(panel)

