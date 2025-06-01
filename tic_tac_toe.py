import tkinter as tk
from tkinter import messagebox, font
import random
from functools import partial
import time

class TicTacToe:
    def __init__(self, root):
        """Initialize the game with main window and default settings"""
        self.root = root
        self.root.title(" Tic Tac Toe BY Ahmed Sherif ")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
       
        self.current_player = "X"
        self.board = [""] * 9
        self.game_mode = "PvP"  
        self.ai_difficulty = "Hard"  # Default difficulty
        self.x_wins = 0
        self.o_wins = 0
        self.ties = 0
        
        # Modern color scheme
        self.bg_color = "#2c3e50"
        self.button_bg = "#34495e"
        self.button_fg = "#ecf0f1"
        self.button_active_bg = "#2c3e50"
        self.x_color = "#e74c3c"  # Red for X
        self.o_color = "#3498db"  # Blue for O
        self.highlight_color = "#f1c40f"
        self.text_color = "#ecf0f1"
        self.win_highlight = "#27ae60"
        
        # Animation variables
        self.animating = False
        self.animation_frames = 10
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create all UI elements"""
        self.root.configure(bg=self.bg_color)
        
        # Title frame
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=(10, 5))
        
        # Stylish title with gradient would be complex, so we'll use a nice font
        try:
            title_font = font.Font(family="Helvetica", size=24, weight="bold")
        except:
            title_font = font.Font(size=24, weight="bold")
            
        tk.Label(title_frame, text="TIC TAC TOE", 
                font=title_font, bg=self.bg_color, fg=self.highlight_color).pack()
        
        # Score display
        score_frame = tk.Frame(self.root, bg=self.bg_color)
        score_frame.pack(pady=5)
        
        self.score_label = tk.Label(score_frame, 
                                  text=f"X: {self.x_wins}  |  O: {self.o_wins}  |  Ties: {self.ties}",
                                  font=("Arial", 12), bg=self.bg_color, fg=self.text_color)
        self.score_label.pack()
        
        # Game mode selection frame
        mode_frame = tk.Frame(self.root, bg=self.bg_color)
        mode_frame.pack(pady=10)
        
        tk.Label(mode_frame, text="Game Mode:", font=("Arial", 10), 
                bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT)
        
        self.mode_var = tk.StringVar(value=self.game_mode)
        modes = [("PvP", "PvP"), ("Player vs AI", "PvAI")]
        for text, mode in modes:
            tk.Radiobutton(mode_frame, text=text, variable=self.mode_var, value=mode, 
                         command=self.change_mode, bg=self.bg_color, fg=self.text_color,
                         selectcolor=self.bg_color, activebackground=self.bg_color,
                         activeforeground=self.text_color).pack(side=tk.LEFT, padx=5)
        
        # Difficulty selection (only visible in PvAI mode)
        self.difficulty_frame = tk.Frame(self.root, bg=self.bg_color)
        
        tk.Label(self.difficulty_frame, text="AI Difficulty:", font=("Arial", 10),
                bg=self.bg_color, fg=self.text_color).pack(side=tk.LEFT)
        
        self.difficulty_var = tk.StringVar(value=self.ai_difficulty)
        difficulties = [("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard"), ("Expert", "Expert")]
        for text, diff in difficulties:
            tk.Radiobutton(self.difficulty_frame, text=text, variable=self.difficulty_var, 
                          value=diff, command=self.change_difficulty, bg=self.bg_color, 
                          fg=self.text_color, selectcolor=self.bg_color,
                          activebackground=self.bg_color, activeforeground=self.text_color).pack(side=tk.LEFT, padx=5)
        
        # Game board with a stylish frame
        board_container = tk.Frame(self.root, bg=self.highlight_color, padx=5, pady=5)
        board_container.pack(pady=20)
        
        self.board_frame = tk.Frame(board_container, bg=self.bg_color)
        self.board_frame.pack()
        self.buttons = []
        button_font = font.Font(family="Arial", size=32, weight="bold")
        for i in range(9):
            row, col = divmod(i, 3)
            btn = tk.Button(self.board_frame, text="", font=button_font, width=3, height=1,
                           bg=self.button_bg, fg=self.text_color, activebackground=self.button_active_bg,
                           relief="ridge", bd=3, command=partial(self.on_click, i))
            btn.grid(row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10)
            self.buttons.append(btn)
            
            # Bind hover effects
            btn.bind("<Enter>", lambda e, b=btn: self.on_hover(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(e, b))
        
        self.status_label = tk.Label(self.root, text=f"Player {self.current_player}'s turn", 
                                    font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.text_color)
        self.status_label.pack(pady=10)
        
        reset_btn = tk.Button(self.root, text="New Game", command=self.reset_game, 
                             font=("Arial", 12), bg="#e74c3c", fg=self.text_color,
                             activebackground="#c0392b", activeforeground=self.text_color,
                             relief="raised", bd=3, padx=15, pady=5)
        reset_btn.pack(pady=10)
        
        
        self.change_mode()
    
    def on_hover(self, event, button):
        """Handle hover effect on buttons"""
        if button["state"] == tk.NORMAL and not self.animating:
            button.config(bg="#3d566e")
    
    def on_leave(self, event, button):
        """Handle leave effect on buttons"""
        if button["state"] == tk.NORMAL and not self.animating:
            button.config(bg=self.button_bg)
    
    def change_mode(self):
        """Show/hide difficulty options based on game mode"""
        self.game_mode = self.mode_var.get()
        if self.game_mode == "PvAI":
            self.difficulty_frame.pack(pady=10)
        else:
            self.difficulty_frame.pack_forget()
        self.reset_game()
    
    def change_difficulty(self):
        """Update AI difficulty level"""
        self.ai_difficulty = self.difficulty_var.get()
    
    def on_click(self, position):
        """Handle player move when a button is clicked"""
        if self.animating:
            return
            
        if self.board[position] == "" and not self.check_game_over():
            self.animate_button_press(position)
            self.make_move(position, self.current_player)
            
            # If in PvAI mode and game isn't over, let AI make a move
            if self.game_mode == "PvAI" and not self.check_game_over():
                self.root.after(500, self.ai_move)
    
    def animate_button_press(self, position):
        """Animate the button press"""
        self.animating = True
        btn = self.buttons[position]
        original_bg = btn.cget("bg")
        
        for i in range(self.animation_frames):
            # Calculate intermediate color
            factor = i / self.animation_frames
            r = int((1 - factor) * int(original_bg[1:3], 16) + factor * int(self.highlight_color[1:3], 16))
            g = int((1 - factor) * int(original_bg[3:5], 16) + factor * int(self.highlight_color[3:5], 16))
            b = int((1 - factor) * int(original_bg[5:7], 16) + factor * int(self.highlight_color[5:7], 16))
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            self.root.after(i * 20, lambda c=color: btn.config(bg=c))
        
        self.root.after(self.animation_frames * 20, lambda: self.finish_animation(position, original_bg))
    
    def finish_animation(self, position, original_bg):
        """Finish the animation sequence"""
        self.animating = False
        self.buttons[position].config(bg=original_bg)
    
    def make_move(self, position, player):
        """Update the board with the player's move"""
        self.board[position] = player
        color = self.x_color if player == "X" else self.o_color
        self.buttons[position].config(text=player, fg=color, state=tk.DISABLED)
        
        # Check if game is over after this move
        if self.check_win(player):
            self.handle_win(player)
            return
        
        if self.check_tie():
            self.handle_tie()
            return
        
        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Player {self.current_player}'s turn")
    
    def handle_win(self, player):
        """Handle a win condition"""
        if player == "X":
            self.x_wins += 1
        else:
            self.o_wins += 1
        self.score_label.config(text=f"X: {self.x_wins}  |  O: {self.o_wins}  |  Ties: {self.ties}")
        
        self.status_label.config(text=f"Player {player} wins!", fg=self.win_highlight)
        self.highlight_winning_cells()
        
        # Show celebration
        self.celebrate_win()
    
    def handle_tie(self):
        """Handle a tie condition"""
        self.ties += 1
        self.score_label.config(text=f"X: {self.x_wins}  |  O: {self.o_wins}  |  Ties: {self.ties}")
        self.status_label.config(text="It's a tie!", fg=self.highlight_color)
    
    def celebrate_win(self):
        """Add some celebration effects for the winner"""
        for btn in self.buttons:
            if btn["text"] == self.current_player:
                self.flash_button(btn)
    
    def flash_button(self, button):
        """Flash a button to celebrate win"""
        original_color = button.cget("fg")
        for i in range(3):  # Flash 3 times
            self.root.after(300 * i, lambda: button.config(fg=self.highlight_color))
            self.root.after(300 * i + 150, lambda: button.config(fg=original_color))
    
    def ai_move(self):
        """AI makes a move based on difficulty level"""
        if self.current_player == "O":  # AI is always "O"
            if self.ai_difficulty == "Easy":
                position = self.ai_move_random()
            elif self.ai_difficulty == "Medium":
                position = self.ai_move_smart_random()
            elif self.ai_difficulty == "Hard":
                position = self.ai_move_minimax()
            else:  # Expert
                position = self.ai_move_expert()
            
            self.animate_button_press(position)
            self.make_move(position, "O")
    
    def ai_move_random(self):
        """AI makes a completely random move (easy difficulty)"""
        empty_positions = [i for i, cell in enumerate(self.board) if cell == ""]
        return random.choice(empty_positions)
    
    def ai_move_smart_random(self):
        """AI makes a smarter move (medium difficulty) - tries to win or block if possible"""
     
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_win("O"):
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_win("X"):
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        if self.board[4] == "":
            return 4
    
        return self.ai_move_random()
    
    def ai_move_minimax(self):
        """AI makes the best possible move using minimax algorithm (hard difficulty)"""
        best_score = -float("inf")
        best_move = None
        
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(0, False, -float("inf"), float("inf"))
                self.board[i] = ""
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move
    
    def ai_move_expert(self):
        """Expert AI that uses minimax but occasionally makes suboptimal moves"""
        # 80% chance to use minimax, 20% to use smart random
        if random.random() < 0.8:
            return self.ai_move_minimax()
        else:
            return self.ai_move_smart_random()
    
    def minimax(self, depth, is_maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning to determine best move"""
        if self.check_win("O"):
            return 10 - depth
        if self.check_win("X"):
            return -10 + depth
        if self.check_tie():
            return 0
        
        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "O"
                    score = self.minimax(depth + 1, False, alpha, beta)
                    self.board[i] = ""
                    
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float("inf")
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "X"
                    score = self.minimax(depth + 1, True, alpha, beta)
                    self.board[i] = ""
                    
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score
    
    def check_win(self, player):
        """Check if the specified player has won"""
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                return True
        return False
    
    def check_tie(self):
        """Check if the game is a tie (no empty cells left)"""
        return "" not in self.board and not self.check_win("X") and not self.check_win("O")
    
    def check_game_over(self):
        """Check if the game is over (win or tie)"""
        return self.check_win("X") or self.check_win("O") or self.check_tie()
    
    def highlight_winning_cells(self):
        """Highlight the winning cells with animation"""
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for condition in win_conditions:
            if all(self.board[i] == "X" for i in condition) or all(self.board[i] == "O" for i in condition):
                for i in condition:
                    self.animate_winning_cell(i)
                break
    
    def animate_winning_cell(self, position):
        """Animate the winning cell"""
        btn = self.buttons[position]
        original_color = btn.cget("bg")
        
        for i in range(5):  # Flash 5 times
            self.root.after(200 * i, lambda: btn.config(bg=self.win_highlight))
            self.root.after(200 * i + 100, lambda: btn.config(bg=original_color))
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.current_player = "X"
        self.board = [""] * 9
        
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL, bg=self.button_bg, fg=self.text_color)
        
        self.status_label.config(text=f"Player {self.current_player}'s turn", fg=self.text_color)
        
        # If it's PvAI and AI starts first (as O), make AI move
        if self.game_mode == "PvAI" and self.current_player == "O":
            self.root.after(500, self.ai_move)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("tic_tac_toe.ico")
    except:
        pass
    
    game = TicTacToe(root)
    root.mainloop()