import tkinter as tk
import random
import math

# --- VORTEX-RESONANZ (150px / 4cm) ---
WIDTH, HEIGHT = 150, 414
BG_COLOR = "#0a0a0a"

class LavaLamp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NEXUS_LAVA")
        self.root.overrideredirect(True)
        # Die 150px Breite schmiegt sich rechts an die Trinity an
        self.root.geometry(f"{WIDTH}x{HEIGHT}+3000+0") 
        self.root.attributes("-topmost", True)
        self.root.configure(bg=BG_COLOR)
        
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack()
        
        self.blobs = []
        for _ in range(8):
            size = random.randint(18, 35)
            self.blobs.append({
                'id': self.canvas.create_oval(0, 0, 0, 0, outline=""),
                'x': random.randint(20, WIDTH-20),
                'y': random.randint(0, HEIGHT),
                'speed': random.uniform(0.3, 1.0),
                'size': size,
                'phase': random.uniform(0, 2 * math.pi)
            })
        self.tick = 0
        self.update_lava()

    def update_lava(self):
        self.tick += 0.015 # Sanfte Geschwindigkeit
        # Der magische Morph: Cyan (#00ffff) <-> Violett (#8a2be2)
        r = int(60 + 60 * math.sin(self.tick)) 
        g = int(127 + 127 * math.cos(self.tick * 0.5))
        color = f'#{r:02x}{g:02x}ff'

        for b in self.blobs:
            b['y'] -= b['speed']
            if b['y'] < -b['size']: b['y'] = HEIGHT + b['size']
            
            # Pulsierender Glow-Effekt
            glow = b['size'] + math.sin(self.tick + b['phase']) * 4
            self.canvas.coords(b['id'], b['x']-glow, b['y']-glow, b['x']+glow, b['y']+glow)
            self.canvas.itemconfig(b['id'], fill=color)
        
        self.root.after(35, self.update_lava)

if __name__ == "__main__":
    app = LavaLamp()
    app.root.mainloop()

