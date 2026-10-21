from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 5 or "[AI_TOWN EMPFANGEN]" in text:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    
    # --- SPRINGER-STANDARD: BREITBILD & KOMPAKTHEIT (Identisch zu Grok/Meta) ---
    MAX_UI_WIDTH = 86 
    
    # Schriftfarbe Weiss (Universums-Stil)
    styled_text = Text(text.strip(), style="bright_white", overflow="fold")
    
    panel = Panel(
        styled_text,
        # Titel in Stadt-Grün für klare visuelle Trennung im selben Slot
        title=f"[bold #00FF00]AI_TOWN @ {zeit}[/bold #00FF00]",
        border_style="#00FF00", 
        subtitle="[dim white]AI_Town_Nexus_v1[/dim white]",
        padding=(0, 2), 
        width=MAX_UI_WIDTH,
        expand=False
    )
    
    # Lückenloser Flow ohne Newline-Sprünge
    console.print(panel)
