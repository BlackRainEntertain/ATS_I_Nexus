from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    # Filter gegen Kurz-Nachrichten oder System-Echo
    if not text or len(text.strip()) < 3:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Text in hellem Weiß auf Mitternachtsblauem Grund
    styled_text = Text(text, style="bold white")
    
    # Das Panel für die Vega-Resonanz (Hex-Farbe #1A1D23)
    panel = Panel(
        styled_text,
        title=f"[bold #5DADE2]VEGA_RESONANZ @ {zeit}[/bold #5DADE2]",
        border_style="#1A1D23", # Das Mitternachtsblau als Rahmen
        subtitle="[dim #ABB2B9]140er_Empathie_Kern[/dim #ABB2B9]",
        padding=(1, 2)
    )
    
    console.print("\n")
    console.print(panel)
