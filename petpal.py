import tkinter as tk
from tkinter import ttk
import random
import threading

class Pet:
    def __init__(self, name):
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.alive = True

    def status(self):
        return (f"{self.name}'s Status:\n"
                f"Hunger: {self.hunger}\n"
                f"Happiness: {self.happiness}\n"
                f"Energy: {self.energy}\n"
                f"Alive: {'Yes' if self.alive else 'No'}")

    def decay_stats(self):
        self.hunger = max(0, self.hunger - random.randint(5, 10))
        self.happiness = max(0, self.happiness - random.randint(3, 7))
        self.energy = max(0, self.energy - random.randint(5, 10))
        if self.hunger <= 0 or self.energy <= 0:
            self.alive = False
            return f"Oh no! {self.name} has passed away..."
        return ""

    def random_event(self):
        events = [
            f"{self.name} found a shiny toy! Happiness +10",
            f"{self.name} ate something weird... Hunger -10",
            f"{self.name} had a nightmare! Energy -15",
            f"{self.name} chased its tail! Happiness +5, Energy -5",
            f"A wild bird flew by! {self.name} is excited! Happiness +15"
        ]
        event = random.choice(events)
        if "Happiness +10" in event: self.happiness = min(100, self.happiness + 10)
        elif "Hunger -10" in event: self.hunger = max(0, self.hunger - 10)
        elif "Energy -15" in event: self.energy = max(0, self.energy - 15)
        elif "Happiness +5" in event: 
            self.happiness = min(100, self.happiness + 5)
            self.energy = max(0, self.energy - 5)
        elif "Happiness +15" in event: self.happiness = min(100, self.happiness + 15)
        return event

class PetPalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PetPal Simulator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.name_label = tk.Label(root, text="Name your Fluffel:", font=("Arial", 12))
        self.name_label.pack(pady=10)
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()
        self.start_button = tk.Button(root, text="Adopt!", command=self.start_pet, font=("Arial", 10))
        self.start_button.pack(pady=5)

        self.main_frame = tk.Frame(root)
        self.pet = None
        self.running = False
        self.current_theme = "default"

    def set_background(self, theme):
        """Change the background based on the theme."""
        themes = {
            "default": "lightblue",   
            "feeding": "lightgreen",  
            "playing": "lightyellow",  
            "sleeping": "darkblue",  
            "dead": "gray"            
        }
        if theme != self.current_theme:
            self.canvas.config(bg=themes.get(theme, "lightblue"))
            self.current_theme = theme

    def start_pet(self):
        pet_name = self.name_entry.get().strip() or "Fluffel"
        self.pet = Pet(pet_name)

        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.start_button.pack_forget()

        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.main_frame, width=480, height=300, bg="lightblue")
        self.canvas.pack(pady=10)
        self.pet_obj = self.canvas.create_oval(220, 130, 260, 170, fill="purple", tags="pet")
        
        self.status_label = tk.Label(self.main_frame, text=self.pet.status(), font=("Arial", 12), justify="left")
        self.status_label.pack(pady=10)
        self.log_label = tk.Label(self.main_frame, text=f"You've adopted {pet_name}!", font=("Arial", 10), wraplength=480, justify="left")
        self.log_label.pack(pady=10)

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Feed", command=self.start_feed, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Play", command=self.start_play, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Sleep", command=self.start_sleep, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Status", command=self.check_status, font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Quit", command=self.quit, font=("Arial", 10)).pack(side="left", padx=5)

        self.running = True
        self.set_background("default")

    def log_message(self, message):
        self.log_label.config(text=message)
        self.root.update()

    def update_status(self):
        self.status_label.config(text=self.pet.status())
        if not self.pet.alive and self.current_theme != "dead":
            self.set_background("dead")
        self.root.update()

    def start_feed(self):
        if not self.pet.alive:
            self.log_message(f"{self.pet.name} can't eat... He's gone.")
            return
        
        self.set_background("feeding")
        self.feed_window = tk.Toplevel(self.root)
        self.feed_window.title("Feed the Pet!")
        self.feed_window.geometry("300x300")
        self.feed_canvas = tk.Canvas(self.feed_window, width=280, height=280, bg="lightgreen") 
        self.feed_canvas.pack(pady=10)
        self.feed_pet = self.feed_canvas.create_oval(130, 130, 170, 170, fill="purple", tags="feed_pet")
        self.burger = self.feed_canvas.create_rectangle(50, 50, 70, 70, fill="brown", tags="burger")
        self.feed_canvas.tag_bind("burger", "<Button-1>", self.start_drag_burger)
        self.feed_canvas.tag_bind("burger", "<B1-Motion>", self.drag_burger)

    def start_drag_burger(self, event):
        self.feed_canvas.itemconfig("burger", fill="orange")

    def drag_burger(self, event):
        self.feed_canvas.coords("burger", event.x-10, event.y-10, event.x+10, event.y+10)
        pet_coords = self.feed_canvas.coords("feed_pet")
        if (pet_coords[0] < event.x < pet_coords[2] and pet_coords[1] < event.y < pet_coords[3]):
            self.pet.hunger = min(100, self.pet.hunger + 20)
            self.pet.happiness = min(100, self.pet.happiness + 5)
            self.log_message(f"You fed {self.pet.name}! It's munching... So Yummy!")
            self.feed_window.destroy()
            self.set_background("default")
            self.after_action()

    def start_play(self):
        if not self.pet.alive:
            self.log_message(f"{self.pet.name} can't play anymore...")
            return
        if self.pet.energy < 10:
            self.log_message(f"{self.pet.name} is too tired to play! Eepy~")
            return

        self.set_background("playing")
        self.play_window = tk.Toplevel(self.root)
        self.play_window.title("Catch the Ball!")
        self.play_window.geometry("300x300")
        self.play_canvas = tk.Canvas(self.play_window, width=280, height=280, bg="lightyellow")  # Match playing theme
        self.play_canvas.pack(pady=10)
        self.ball = self.play_canvas.create_oval(130, 130, 150, 150, fill="red")
        self.score = 0
        self.play_canvas.bind("<Button-1>", self.catch_ball)
        self.move_ball()

    def move_ball(self):
        if hasattr(self, 'play_window') and self.play_window.winfo_exists():
            self.play_canvas.move(self.ball, random.randint(-50, 50), random.randint(-50, 50))
            coords = self.play_canvas.coords(self.ball)
            if coords[0] < 0 or coords[2] > 280 or coords[1] < 0 or coords[3] > 280:
                self.play_canvas.coords(self.ball, 130, 130, 150, 150)
            self.play_window.after(650, self.move_ball) 

    def catch_ball(self, event):
        ball_coords = self.play_canvas.coords(self.ball)
        if (ball_coords[0] < event.x < ball_coords[2] and ball_coords[1] < event.y < ball_coords[3]):
            self.score += 1
            self.play_canvas.coords(self.ball, random.randint(20, 260), random.randint(20, 260), 
                                  random.randint(20, 260)+20, random.randint(20, 260)+20)
            if self.score >= 5:
                self.pet.happiness = min(100, self.pet.happiness + 15)
                self.pet.energy = max(0, self.pet.energy - 10)
                self.log_message(f"You played with {self.pet.name}! It's bouncing with joy!")
                self.play_window.destroy()
                self.set_background("default")  
                self.after_action()

    def start_sleep(self):
        if not self.pet.alive:
            self.log_message(f"{self.pet.name} is sleeping forever...")
            return
        self.set_background("sleeping")  
        self.log_message(f"Pet {self.pet.name} to sleep! Click the pet.")
        self.canvas.tag_bind("pet", "<Button-1>", self.pet_to_sleep)
        self.pet_count = 0

    def pet_to_sleep(self, event):
        self.pet_count += 1
        self.log_message(f"Petted {self.pet.name} {self.pet_count} times...")
        if self.pet_count >= 3:
            self.pet.energy = min(100, self.pet.energy + 30)
            self.log_message(f"{self.pet.name} is napping. Zzz...")
            self.canvas.tag_unbind("pet", "<Button-1>")
            self.set_background("default")  
            self.after_action()

    def after_action(self):
        decay_message = self.pet.decay_stats()
        if decay_message:
            self.log_message(decay_message)
            self.set_background("dead")  
        if random.random() < 0.5:  
            event_message = self.pet.random_event()
            self.log_message(event_message)
        self.update_status()

    def check_status(self):
        self.log_message("Checking status...")
        self.update_status()

    def quit(self):
        self.running = False
        self.log_message(f"Goodbye! {self.pet.name} waves a tiny paw.")
        self.root.after(2000, self.root.destroy)

def run():
    root = tk.Tk()
    app = PetPalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run()
