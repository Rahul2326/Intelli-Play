import tkinter as tk
from tkinter import messagebox
import pygame  # For sound effects

# Constants
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Load sound effects
move_sound = pygame.mixer.Sound("shuffle.wav")
win_sound = pygame.mixer.Sound("win.wav")
draw_sound = pygame.mixer.Sound("hint.wav")
reset_sound = pygame.mixer.Sound("sucess.wav")

# Minimax Algorithm (same as before)
def minimax(board, depth, is_maximizing_player, alpha, beta):
    if check_win(board, PLAYER_X):
        return -1  # Player X wins
    if check_win(board, PLAYER_O):
        return 1  # Player O wins
    if is_board_full(board):
        return 0  # Draw

    if is_maximizing_player:
        max_eval = float('-inf')
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_O
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[i] = EMPTY
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_X
                eval = minimax(board, depth + 1, True, alpha, beta)
                board[i] = EMPTY
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

# Function to get the best move for AI
def get_best_move(board):
    best_move = None
    best_value = float('-inf')

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = PLAYER_O
            move_value = minimax(board, 0, False, float('-inf'), float('inf'))
            board[i] = EMPTY
            if move_value > best_value:
                best_value = move_value
                best_move = i
    return best_move

# Function to check if the board is full
def is_board_full(board):
    return EMPTY not in board

# Function to check for a win
def check_win(board, player):
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)]
    for comb in winning_combinations:
        if board[comb[0]] == board[comb[1]] == board[comb[2]] == player:
            return True
    return False

# Function to handle button click
def button_click(i):
    if board[i] == EMPTY and not game_over:
        board[i] = PLAYER_X
        buttons[i].config(text=PLAYER_X, state="disabled", disabledforeground="blue")
        move_sound.play()  # Play move sound
        
        if check_win(board, PLAYER_X):
            win_sound.play()  # Play win sound
            messagebox.showinfo("Game Over", "Player X wins!")
            disable_all_buttons()
            return
        elif is_board_full(board):
            draw_sound.play()  # Play draw sound
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_all_buttons()
            return

        # AI move
        ai_move = get_best_move(board)
        board[ai_move] = PLAYER_O
        buttons[ai_move].config(text=PLAYER_O, state="disabled", disabledforeground="red")
        move_sound.play()  # Play move sound

        if check_win(board, PLAYER_O):
            win_sound.play()  # Play win sound
            messagebox.showinfo("Game Over", "Player O wins!")
            disable_all_buttons()
            return
        elif is_board_full(board):
            draw_sound.play()  # Play draw sound
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_all_buttons()
            return

# Function to disable all buttons
def disable_all_buttons():
    global game_over
    game_over = True
    for button in buttons:
        button.config(state="disabled")

# Function to reset the game
def reset_game():
    global board, game_over
    reset_sound.play()  # Play reset sound
    board = [EMPTY] * 9
    game_over = False
    for button in buttons:
        button.config(text="", state="normal", disabledforeground="black")

# Initialize the main window
root = tk.Tk()
root.title("Fancy Tic-Tac-Toe with Minimax AI")

# Set a custom background color
root.configure(bg="black")

# Board and game state
board = [EMPTY] * 9
game_over = False

# Create a 3x3 grid of buttons with fancy styling
buttons = []
for i in range(9):
    button = tk.Button(root, text="", width=10, height=3, font=("Arial", 36, "bold"),
                       relief="solid", bg="lightgray", activebackground="darkgray",
                       command=lambda i=i: button_click(i))
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(button)

# Reset button
reset_button = tk.Button(root, text="Reset", font=("Arial", 16, "bold"), command=reset_game,
                         bg="green", fg="white", activebackground="darkgreen", relief="raised")
reset_button.grid(row=3, column=0, columnspan=3, pady=20)

# Run the Tkinter event loop
root.mainloop()
