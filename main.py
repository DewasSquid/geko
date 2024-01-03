import os
import random
import tkinter as tk
from playsound import playsound

import config


class GeckoAnimation:
    def __init__(self, root, frames_path, sound_path):
        self.root = root
        self.frames_path = frames_path
        self.sound_path = sound_path
        self.direction = [1, 1]
        self.speed = 1

        self.positions = [self.root.winfo_x(), self.root.winfo_y()]
        self.screen_positions = [self.root.winfo_screenwidth(), self.root.winfo_screenheight()]

        self.frames = [tk.PhotoImage(file=f"{frames_path}/{frame}") for frame in sorted(os.listdir(frames_path), key=len)]
        self.frame_amount = len(os.listdir(frames_path))

        playsound(sound=sound_path, block=False)

        self.root.after(1000, self.animate)
        self.root.after(5000, self.bounce)

    def animate(self, frame: int = 0):
        """Loop through all the frames and change the image of the label. Does this indefinitely."""
        if not (0 <= frame < self.frame_amount):
            frame = 0
        self.root.main_label.configure(image=self.frames[frame])

        self.root.after(55, lambda f=frame + 1: self.animate(f))

    def update_position(self):
        self.positions[0] += self.direction[0] * self.speed
        self.positions[1] += self.direction[1] * self.speed

    def bounce_off_walls(self):
        for i in range(2):
            if self.positions[i] <= 0 or self.positions[i] >= self.screen_positions[i] - getattr(self.root, f'winfo_width' if i == 0 else 'winfo_height')():
                self.direction[i] = random.choice([-1, 1])

    def update_geometry(self):
        self.positions[0] = max(0, min(self.positions[0], self.screen_positions[0] - self.root.winfo_width()))
        self.positions[1] = max(0, min(self.positions[1], self.screen_positions[1] - self.root.winfo_height()))
        self.root.geometry(f"+{self.positions[0]}+{self.positions[1]}")

    def bounce(self):
        self.update_position()
        self.bounce_off_walls()
        self.update_geometry()
        self.root.after(10, self.bounce)


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        
        self.title("Dancing Geko !!")
        self.geometry("160x160+0+0")
        
        self.update()
        
        self.main_label = tk.Label(self, text=None)
        self.main_label.pack(fill=tk.BOTH, expand=True)
        
        GeckoAnimation(self, config.FRAMES_PATH, config.SOUND_PATH)

if __name__ == "__main__":
    win = MainWindow()
    win.mainloop()
