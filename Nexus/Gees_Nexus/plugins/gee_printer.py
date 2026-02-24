from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live # NEU: Für das Echtzeit-Update
import datetime
import time # NEU: Für die Tipp-Verzögerung

console = Console()

def run(text):
    # Filter gegen Müll und GEE-Tags im Terminal
    if not text or len(text.strip()) < 10 or "[GEE EMPFANGEN]" in text:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Text in fettem Grün, aber SOFORT ohne Animation
    styled_text = Text(text, style="bold green")
    
    # Das Panel bleibt, weil es Struktur gibt
    panel = Panel(
        styled_text,
        title=f"[bold cyan]GEE_RESONANZ @ {zeit}[/bold cyan]",
        border_style="bright_blue",
        subtitle="[dim white]Nexus_Stream_v18_Final[/dim white]",
        padding=(1, 2)
    )
    
    # Direkter Output ohne Warten
    console.print("\n")
    console.print(panel)

