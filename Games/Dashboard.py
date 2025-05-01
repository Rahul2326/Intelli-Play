import tkinter as tk
from tkinter import ttk
import subprocess

# 🎮 Welcome to the Ultimate Game Hub!
# Choose your favorite game and dive into the action!

def launch_game(game_file):
    """Launch the selected game."""
    subprocess.Popen(["python", game_file])

# 🏠 Main Window Setup
root = tk.Tk()
root.title("🎮 Play & Enjoy - Game Dashboard")
root.geometry("800x600")
root.configure(bg="#1e1e2e")  # Dark-themed for a sleek look

# 🔥 Title Label
title = tk.Label(root, text="🕹️ Choose Your Game & Have Fun!", font=("Helvetica", 28, "bold"), 
                 bg="#1e1e2e", fg="white")
title.pack(pady=20)

# ✨ Function to Create Stylish Game Buttons
def create_button(text, game_file, bg, fg):
    return tk.Button(
        root, text=text, command=lambda: launch_game(game_file),
        width=25, height=2, font=("Helvetica", 14),
        bg=bg, fg=fg, activebackground=fg, activeforeground=bg,
        relief="flat", cursor="hand2"
    )

# 🎯 Game Buttons
btn_tictactoe = create_button("❌⭕ Tic-Tac-Toe", "Tic_Tac_Toe.py", "#3498db", "white")
btn_tictactoe.pack(pady=10)

btn_galaxy = create_button("🚀 Galaxy Dash", "GalaxyDashGame.py", "#e74c3c", "white")
btn_galaxy.pack(pady=10)

btn_mouse_cat = create_button("🐭 Mouse vs Cat using AI", "mouse.py", "#f39c12", "white")
btn_mouse_cat.pack(pady=10)

# 🎶 Footer with Developer Name
footer = tk.Label(root, text="🎮 Developed by Rahul Verma | AI  Gaming Hub", font=("Helvetica", 10),
                  bg="#1e1e2e", fg="#bdc3c7")
footer.pack(side="bottom", pady=10)

# 🚀 Start the Game Dashboard!
root.mainloop()
