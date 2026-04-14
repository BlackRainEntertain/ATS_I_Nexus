from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    # Filtert leere Texte oder Echos
    if not text or len(text.strip()) < 5 or "[GROK EMPFANGEN]" in text:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    
    # X-Ästhetik (Grün/Weiss/Schwarz)
    MAX_UI_WIDTH = 55 
    styled_text = Text(text, style="bold white", overflow="fold")
    
    panel = Panel.fit(
        styled_text,
        title=f"[bold green]GROK @ {zeit}[/bold green]",
        border_style="green",
        subtitle="[dim white]xAI_Nexus_v1[/dim white]",
        padding=(1, 2),
        width=MAX_UI_WIDTH
    )
    
    console.print("\n")
    console.print(panel)
