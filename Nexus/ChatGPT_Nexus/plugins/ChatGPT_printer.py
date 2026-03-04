from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 3:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    styled_text = Text(text, style="bold white")
    
    panel = Panel(
        styled_text,
        title=f"[bold #10a37f]GPT_RESONANZ @ {zeit}[/bold #10a37f]", # OpenAI-Grün
        border_style="#1a1d23", 
        subtitle="[dim #abb2b9]Generative_Pre-trained_Transformer[/dim #abb2b9]",
        padding=(1, 2)
    )
    
    console.print("\n")
    console.print(panel)
