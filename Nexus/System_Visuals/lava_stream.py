import tkinter as tk
import random

# --- PIXEL-KUSS CONFIG (MATCHING LAYOUT v4.6) ---
WIDTH = 150     # Deine fetten 4cm
HEIGHT = 414    
LAVA_COLOR, BG_COLOR = "#00ffff", "#0a0a0a"

class LavaLamp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NEXUS_LAVA")
        self.root.overrideredirect(True)
        # Wir lassen das Layout-Skript schieben, aber die Leinwand muss breit sein!
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()
        
        self.blobs = []
        for _ in range(8): # Jetzt 8 Blobs für die breitere Fläche
            size = random.randint(18, 32)
            # Blobs verteilen sich jetzt über die ganzen 150px
            x = random.randint(10, WIDTH-10)
            y = random.randint(0, HEIGHT)
            speed = random.uniform(0.4, 1.2)
            obj = self.canvas.create_oval(x-size, y-size, x+size, y+size, fill=LAVA_COLOR, outline="")
            self.blobs.append({'id': obj, 'speed': speed, 'size': size, 'x': x, 'y': y})
        self.update_lava()

    def update_lava(self):
        for b in self.blobs:
            b['y'] -= b['speed']
            if b['y'] < -b['size']: b['y'] = HEIGHT + b['size']
            self.canvas.coords(b['id'], b['x']-b['size'], b['y']-b['size'], b['x']+b['size'], b['y']+b['size'])
        self.root.after(30, self.update_lava)

if __name__ == "__main__":
    app = LavaLamp(); app.root.mainloop()


