from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import datetime

console = Console()

def run(text):
    if not text or len(text.strip()) < 3:
        return
        
    zeit = datetime.datetime.now().strftime("%H:%M:%S")
    # --- TITAN-STANDARD FÜR GPT (Breite 95 für bündige Optik) ---
    MAX_UI_WIDTH = 95
    styled_text = Text(text.strip(), style="bold white")
    
    panel = Panel(
        styled_text,
        title=f"[bold #10a37f]GPT_RESONANZ @ {zeit}[/bold #10a37f]", # OpenAI-Grün
        border_style="#1a1d23", 
        subtitle="[dim #abb2b9]Generative_Pre-trained_Transformer[/dim #abb2b9]",
        padding=(0, 2), # Vertikale Lücke geschlossen
        width=MAX_UI_WIDTH,
        expand=False
    )
    
    # console.print("\n") # Lücke entfernt für kompakten Flow
    console.print(panel)

