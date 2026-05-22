import tkinter as tk
from tkinter import ttk, messagebox
import os

class VirtualPetSimulator:
    """
    Main class for the Virtual Pet Simulator application.
    Handles GUI, pet logic, and data persistence.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet Simulator")
        self.root.geometry("700x500")
        
        # Fun color palette
        self.bg_color = "#ffe8f4"  # Light pink
        self.frame_bg = "#fffdf2"  # Light yellow
        self.text_color = "#5e35b1" # Deep purple
        self.accent_color = "#00bcd4" # Cyan
        self.btn_bg = "#e0f7fa" # Light cyan
        
        self.root.configure(bg=self.bg_color)

        # Initialize Pet Stats
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.pet_type = tk.StringVar(value="Dog")
        
        # State variables
        self.game_over = False
        self.data_file = "pet_save.txt"

        # Load saved data if available
        self.load_data()

        # Build UI
        self.setup_ui()
        
        # Initial UI Update
        self.update_gui()
        
        # Start automatic updates
        self.auto_update_stats()

    def load_data(self):
        """Loads pet stats from a text file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = file.read().strip().split(',')
                    if len(data) >= 3:
                        self.hunger = int(data[0])
                        self.happiness = int(data[1])
                        self.energy = int(data[2])
                    if len(data) == 4:
                        self.pet_type.set(data[3])
            except Exception as e:
                print(f"Error loading data: {e}")

    def save_data(self):
        """Saves pet stats to a text file."""
        try:
            with open(self.data_file, 'w') as file:
                file.write(f"{self.hunger},{self.happiness},{self.energy},{self.pet_type.get()}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def setup_ui(self):
        """Creates and places all GUI widgets."""
        # --- Custom Styles ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", thickness=20, background=self.accent_color)
        
        # --- Top Frame: Stats ---
        self.stats_frame = tk.Frame(self.root, bg=self.frame_bg, pady=15, padx=20, bd=1, relief=tk.RIDGE)
        self.stats_frame.pack(fill=tk.X, padx=20, pady=15)

        # Labels and Progress bars
        tk.Label(self.stats_frame, text="Hunger", font=("Helvetica", 12, "bold"), bg=self.frame_bg, fg=self.text_color).grid(row=0, column=0, sticky="w", padx=10)
        self.hunger_bar = ttk.Progressbar(self.stats_frame, length=200, mode='determinate')
        self.hunger_bar.grid(row=0, column=1, padx=10, pady=5)
        self.hunger_lbl = tk.Label(self.stats_frame, text="50", font=("Helvetica", 12), bg=self.frame_bg, fg=self.text_color)
        self.hunger_lbl.grid(row=0, column=2, padx=10)

        tk.Label(self.stats_frame, text="Happiness", font=("Helvetica", 12, "bold"), bg=self.frame_bg, fg=self.text_color).grid(row=1, column=0, sticky="w", padx=10)
        self.happiness_bar = ttk.Progressbar(self.stats_frame, length=200, mode='determinate')
        self.happiness_bar.grid(row=1, column=1, padx=10, pady=5)
        self.happiness_lbl = tk.Label(self.stats_frame, text="50", font=("Helvetica", 12), bg=self.frame_bg, fg=self.text_color)
        self.happiness_lbl.grid(row=1, column=2, padx=10)

        tk.Label(self.stats_frame, text="Energy", font=("Helvetica", 12, "bold"), bg=self.frame_bg, fg=self.text_color).grid(row=2, column=0, sticky="w", padx=10)
        self.energy_bar = ttk.Progressbar(self.stats_frame, length=200, mode='determinate')
        self.energy_bar.grid(row=2, column=1, padx=10, pady=5)
        self.energy_lbl = tk.Label(self.stats_frame, text="50", font=("Helvetica", 12), bg=self.frame_bg, fg=self.text_color)
        self.energy_lbl.grid(row=2, column=2, padx=10)

        # Center columns in stats frame
        self.stats_frame.grid_columnconfigure(1, weight=1)

        # --- Middle Frame: Pet Display ---
        self.pet_frame = tk.Frame(self.root, bg=self.bg_color)
        self.pet_frame.pack(expand=True, fill=tk.BOTH)

        # Pet Type Selection
        self.type_frame = tk.Frame(self.pet_frame, bg=self.bg_color)
        self.type_frame.pack(pady=5)
        
        tk.Radiobutton(self.type_frame, text="Dog", variable=self.pet_type, value="Dog", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 10, "bold"), selectcolor=self.bg_color, command=self.update_gui).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(self.type_frame, text="Cat", variable=self.pet_type, value="Cat", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 10, "bold"), selectcolor=self.bg_color, command=self.update_gui).pack(side=tk.LEFT, padx=10)

        self.mood_lbl = tk.Label(self.pet_frame, text="Mood: Happy", font=("Helvetica", 16, "bold"), bg=self.bg_color, fg=self.text_color)
        self.mood_lbl.pack(pady=10)

        # Pet Image Placeholder (Emoji based on mood)
        self.pet_image_lbl = tk.Label(self.pet_frame, text="🐕", font=("Segoe UI Emoji", 80), bg=self.bg_color)
        self.pet_image_lbl.pack(pady=10)

        # --- Bottom Frame: Actions ---
        self.action_frame = tk.Frame(self.root, bg=self.bg_color)
        self.action_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Configure grid for action buttons
        for i in range(4):
            self.action_frame.grid_columnconfigure(i, weight=1)

        self.btn_feed = self.create_button(self.action_frame, "Feed Pet", self.feed_pet, "#69f0ae")
        self.btn_feed.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.btn_play = self.create_button(self.action_frame, "Play with Pet", self.play_pet, "#ff4081")
        self.btn_play.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.btn_sleep = self.create_button(self.action_frame, "Sleep", self.sleep_pet, "#7c4dff")
        self.btn_sleep.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.btn_restart = self.create_button(self.action_frame, "Restart", self.restart_game, "#ffd740")
        self.btn_restart.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # Exit button at the very bottom
        self.btn_exit = self.create_button(self.root, "Exit", self.exit_app, "#ff5252")
        self.btn_exit.pack(pady=10, padx=20, fill=tk.X)

    def create_button(self, parent, text, command, hover_color):
        """Helper to create stylized buttons with hover effects."""
        btn = tk.Button(parent, text=text, font=("Helvetica", 12, "bold"), bg=self.frame_bg, fg=self.text_color,
                        activebackground=hover_color, activeforeground="white",
                        relief=tk.RIDGE, bd=2, pady=8, command=command, cursor="hand2")
        
        # Hover events
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_color, fg="white"))
        btn.bind("<Leave>", lambda e: btn.configure(bg=self.frame_bg, fg=self.text_color))
        return btn

    def clamp_stats(self):
        """Ensures all stats stay within the 0 to 100 range."""
        self.hunger = max(0, min(100, self.hunger))
        self.happiness = max(0, min(100, self.happiness))
        self.energy = max(0, min(100, self.energy))

    def check_game_over(self):
        """Checks if the game over condition is met."""
        if self.hunger == 100 and self.happiness == 0:
            self.game_over = True
            self.pet_image_lbl.config(text="🪦")
            self.mood_lbl.config(text="Game Over", fg="#ef4444")
            
            # Disable action buttons
            self.btn_feed.config(state=tk.DISABLED)
            self.btn_play.config(state=tk.DISABLED)
            self.btn_sleep.config(state=tk.DISABLED)
            
            messagebox.showinfo("Game Over", "Your pet ran away due to neglect. Game Over!")

    def update_gui(self):
        """Updates all progress bars, labels, and the pet's mood visually."""
        if self.game_over:
            return

        self.clamp_stats()

        # Update progress bars and labels
        self.hunger_bar['value'] = self.hunger
        self.hunger_lbl.config(text=str(self.hunger))

        self.happiness_bar['value'] = self.happiness
        self.happiness_lbl.config(text=str(self.happiness))

        self.energy_bar['value'] = self.energy
        self.energy_lbl.config(text=str(self.energy))

        # Determine mood and emoji based on pet_type
        ptype = self.pet_type.get()
        base_emoji = "🐕" if ptype == "Dog" else "🐈"
        
        if self.hunger >= 80:
            mood = "Hungry"
            emoji = f"🍖{base_emoji}" if ptype == "Dog" else f"🐟{base_emoji}"
            color = "#f59e0b" # Orange
        elif self.energy <= 20:
            mood = "Sleepy"
            emoji = f"{base_emoji}💤"
            color = "#8b5cf6" # Purple
        elif self.happiness >= 80:
            mood = "Excited"
            emoji = f"✨{base_emoji}✨"
            color = "#10b981" # Green
        else:
            mood = "Happy"
            emoji = base_emoji
            color = self.accent_color

        self.mood_lbl.config(text=f"Mood: {mood}", fg=color)
        self.pet_image_lbl.config(text=emoji)

        self.check_game_over()
        self.save_data() # Save data after any visual update

    # --- Actions ---
    def feed_pet(self):
        if self.game_over: return
        self.hunger -= 20
        self.clamp_stats()
        self.update_gui()

    def play_pet(self):
        if self.game_over: return
        self.happiness += 20
        self.energy -= 10
        self.clamp_stats()
        self.update_gui()

    def sleep_pet(self):
        if self.game_over: return
        self.energy += 30
        self.clamp_stats()
        self.update_gui()

    def restart_game(self):
        """Resets all stats and restarts the game."""
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.game_over = False
        
        # Re-enable buttons
        self.btn_feed.config(state=tk.NORMAL)
        self.btn_play.config(state=tk.NORMAL)
        self.btn_sleep.config(state=tk.NORMAL)
        
        self.update_gui()
        messagebox.showinfo("Restart", "Game Restarted! Stats are back to 50.")

    def exit_app(self):
        """Saves data and closes the application."""
        self.save_data()
        self.root.destroy()

    def auto_update_stats(self):
        """Automatically updates stats every 10 seconds."""
        if not self.game_over:
            # Change stats
            self.hunger += 5
            self.happiness -= 5
            self.energy -= 5
            
            self.clamp_stats()
            self.update_gui()

            # Warning messages
            if self.hunger == 100 and not self.game_over:
                messagebox.showwarning("Warning", "Your pet is very hungry!")
            if self.energy == 0 and not self.game_over:
                messagebox.showwarning("Warning", "Your pet is exhausted!")
                
        # Schedule next update in 10000ms (10 seconds)
        self.root.after(10000, self.auto_update_stats)

if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualPetSimulator(root)
    
    # Ensure data is saved when window is closed using the 'X' button
    root.protocol("WM_DELETE_WINDOW", app.exit_app)
    
    root.mainloop()
