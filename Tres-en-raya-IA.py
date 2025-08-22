import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import math
import threading
from typing import List, Tuple, Optional

class AdvancedTicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Tres en Raya BRUTAL - by Edilson")
        self.root.geometry("1000x800")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)  # Permitir redimensionar
        
        # Centrar la ventana en la pantalla
        self.center_window()
        
        # Game variables
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_mode = 'vs_ai'  # 'vs_player', 'vs_ai', 'ai_vs_ai'
        self.difficulty = 'impossible'  # 'easy', 'medium', 'hard', 'impossible'
        self.game_over = False
        self.scores = {'X': 0, 'O': 0, 'Draw': 0}
        self.move_count = 0
        self.thinking_time = 1.0
        
        # Animation variables
        self.animation_speed = 100
        self.winning_line = None
        
        # Colors and themes
        self.colors = {
            'bg': '#0a0a0a',
            'primary': '#00ff88',
            'secondary': '#0080ff',
            'accent': '#ff0080',
            'text': '#ffffff',
            'button_bg': '#1a1a1a',
            'button_hover': '#2a2a2a',
            'grid': '#333333'
        }
        
        self.setup_ui()
        self.create_game_board()
        self.update_status()
        
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = 1000
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Setup the main UI components"""
        # Title
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=(10, 5))
        
        title_label = tk.Label(
            title_frame, 
            text="🎮 TRES EN RAYA BRUTAL 🎮",
            font=('Arial', 20, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Powered by Advanced AI & Neural Networks",
            font=('Arial', 10),
            fg=self.colors['secondary'],
            bg=self.colors['bg']
        )
        subtitle.pack()
        
        # Control panel
        self.create_control_panel()
        
        # Game board frame
        self.game_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.game_frame.pack(pady=(10, 15))
        
        # Status and scores
        self.create_status_panel()
        
    def create_control_panel(self):
        """Create control panel with game options"""
        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(pady=(5, 10))
        
        # Game mode selection
        mode_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        mode_frame.pack(side=tk.LEFT, padx=15)
        
        tk.Label(
            mode_frame, 
            text="Modo de Juego:",
            font=('Arial', 11, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        ).pack()
        
        mode_var = tk.StringVar(value=self.game_mode)
        modes = [
            ('👥 Jugador vs Jugador', 'vs_player'),
            ('🤖 Jugador vs IA', 'vs_ai'),
            ('🔥 IA vs IA (Espectáculo)', 'ai_vs_ai')
        ]
        
        for text, mode in modes:
            tk.Radiobutton(
                mode_frame,
                text=text,
                variable=mode_var,
                value=mode,
                command=lambda m=mode: self.change_game_mode(m),
                font=('Arial', 9),
                fg=self.colors['text'],
                bg=self.colors['bg'],
                selectcolor=self.colors['button_bg'],
                activebackground=self.colors['button_hover'],
                activeforeground=self.colors['primary']
            ).pack(anchor='w')
        
        # Difficulty selection
        diff_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        diff_frame.pack(side=tk.LEFT, padx=15)
        
        tk.Label(
            diff_frame,
            text="Dificultad IA:",
            font=('Arial', 11, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg']
        ).pack()
        
        diff_var = tk.StringVar(value=self.difficulty)
        difficulties = [
            ('😴 Fácil (Random)', 'easy'),
            ('🤔 Medio (Básico)', 'medium'),
            ('😤 Difícil (Inteligente)', 'hard'),
            ('🔥 IMPOSIBLE (Minimax)', 'impossible')
        ]
        
        for text, diff in difficulties:
            tk.Radiobutton(
                diff_frame,
                text=text,
                variable=diff_var,
                value=diff,
                command=lambda d=diff: self.change_difficulty(d),
                font=('Arial', 9),
                fg=self.colors['text'],
                bg=self.colors['bg'],
                selectcolor=self.colors['button_bg'],
                activebackground=self.colors['button_hover'],
                activeforeground=self.colors['secondary']
            ).pack(anchor='w')
        
        # Action buttons
        button_frame = tk.Frame(control_frame, bg=self.colors['bg'])
        button_frame.pack(side=tk.LEFT, padx=15)
        
        self.create_gradient_button(
            button_frame, 
            "🔄 Nueva Partida", 
            self.new_game,
            self.colors['primary']
        ).pack(pady=3)
        
        self.create_gradient_button(
            button_frame,
            "📊 Estadísticas",
            self.show_stats,
            self.colors['secondary']
        ).pack(pady=3)
        
        self.create_gradient_button(
            button_frame,
            "❌ Salir",
            self.root.quit,
            self.colors['accent']
        ).pack(pady=3)
    
    def create_gradient_button(self, parent, text, command, color):
        """Create a modern gradient button"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=('Arial', 10, 'bold'),
            fg='white',
            bg=color,
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2'
        )
        
        # Hover effects
        def on_enter(e):
            button.config(bg=self.lighten_color(color))
        
        def on_leave(e):
            button.config(bg=color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def lighten_color(self, color):
        """Lighten a hex color"""
        # Simple color lightening
        if color == self.colors['primary']:
            return '#33ff99'
        elif color == self.colors['secondary']:
            return '#3399ff'
        elif color == self.colors['accent']:
            return '#ff3399'
        return color
    
    def create_game_board(self):
        """Create the interactive game board"""
        self.buttons = []
        board_frame = tk.Frame(self.game_frame, bg=self.colors['bg'])
        board_frame.pack()
        
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    board_frame,
                    text='',
                    font=('Arial', 28, 'bold'),
                    width=5,
                    height=2,
                    bg=self.colors['button_bg'],
                    fg=self.colors['text'],
                    relief='raised',
                    bd=3,
                    command=lambda r=i, c=j: self.make_move(r, c),
                    cursor='hand2'
                )
                button.grid(row=i, column=j, padx=3, pady=3)
                
                # Hover effects
                button.bind("<Enter>", lambda e, b=button: self.button_hover(b, True))
                button.bind("<Leave>", lambda e, b=button: self.button_hover(b, False))
                
                row.append(button)
            self.buttons.append(row)
    
    def button_hover(self, button, entering):
        """Handle button hover effects"""
        if entering:
            button.config(bg=self.colors['button_hover'])
        else:
            # Don't change color if button has been played
            if button['text'] == '':
                button.config(bg=self.colors['button_bg'])
    
    def create_status_panel(self):
        """Create status and score panel"""
        status_frame = tk.Frame(self.root, bg=self.colors['bg'])
        status_frame.pack(pady=(10, 20))
        
        # Current player indicator
        self.status_label = tk.Label(
            status_frame,
            text="",
            font=('Arial', 14, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['bg']
        )
        self.status_label.pack(pady=3)
        
        # Thinking indicator (for AI)
        self.thinking_label = tk.Label(
            status_frame,
            text="",
            font=('Arial', 11),
            fg=self.colors['secondary'],
            bg=self.colors['bg']
        )
        self.thinking_label.pack()
        
        # Scores
        score_frame = tk.Frame(status_frame, bg=self.colors['bg'])
        score_frame.pack(pady=8)
        
        self.score_label = tk.Label(
            score_frame,
            text="",
            font=('Arial', 12),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        self.score_label.pack()
    
    def update_status(self):
        """Update status display"""
        if self.game_over:
            self.status_label.config(text="🎉 ¡Juego Terminado! 🎉")
        elif self.game_mode == 'ai_vs_ai':
            self.status_label.config(text=f"🤖 IA Turno: {self.current_player}")
        elif self.game_mode == 'vs_ai' and self.current_player == 'O':
            self.status_label.config(text="🤖 IA está pensando...")
        else:
            self.status_label.config(text=f"🎯 Turno del Jugador: {self.current_player}")
        
        # Update scores
        score_text = f"🏆 X: {self.scores['X']} | O: {self.scores['O']} | Empates: {self.scores['Draw']}"
        self.score_label.config(text=score_text)
    
    def make_move(self, row, col):
        """Make a move on the board"""
        if self.game_over or self.board[row][col] != '':
            return
        
        # Prevent human moves during AI thinking
        if self.game_mode == 'vs_ai' and self.current_player == 'O':
            return
        
        self.place_piece(row, col, self.current_player)
        
        if not self.check_game_over():
            self.switch_player()
            
            # AI move
            if self.game_mode == 'vs_ai' and self.current_player == 'O':
                self.root.after(500, self.ai_move)
            elif self.game_mode == 'ai_vs_ai':
                self.root.after(1000, self.ai_move)
    
    def place_piece(self, row, col, player):
        """Place a piece with animation"""
        self.board[row][col] = player
        button = self.buttons[row][col]
        
        # Color based on player
        color = self.colors['primary'] if player == 'X' else self.colors['secondary']
        
        # Animation effect
        button.config(
            text=player,
            fg=color,
            bg=self.colors['button_hover'],
            state='disabled'
        )
        
        # Pulse effect
        self.animate_button(button, color)
        
        self.move_count += 1
        self.update_status()
    
    def animate_button(self, button, color):
        """Animate button placement"""
        original_bg = button['bg']
        
        def pulse(step=0):
            if step < 6:
                alpha = 0.5 + 0.5 * math.sin(step * math.pi / 3)
                # Simple pulse effect by changing relief
                relief = 'sunken' if step % 2 == 0 else 'raised'
                button.config(relief=relief)
                self.root.after(50, lambda: pulse(step + 1))
            else:
                button.config(relief='flat', bg=original_bg)
        
        pulse()
    
    def ai_move(self):
        """Make AI move based on difficulty"""
        if self.game_over:
            return
            
        self.show_thinking_animation()
        
        def make_ai_move():
            if self.difficulty == 'easy':
                move = self.ai_random()
            elif self.difficulty == 'medium':
                move = self.ai_medium()
            elif self.difficulty == 'hard':
                move = self.ai_hard()
            else:  # impossible
                move = self.ai_minimax()
            
            if move:
                row, col = move
                self.root.after(0, lambda: self.place_piece(row, col, self.current_player))
                self.root.after(100, self.check_and_continue)
        
        # Simulate thinking time
        thinking_thread = threading.Thread(target=lambda: (
            time.sleep(self.thinking_time),
            make_ai_move()
        ))
        thinking_thread.daemon = True
        thinking_thread.start()
    
    def show_thinking_animation(self):
        """Show AI thinking animation"""
        dots = ""
        
        def animate_thinking(count=0):
            nonlocal dots
            if count < 10 and not self.game_over:  # Stop if game ends
                dots = "." * ((count % 3) + 1)
                self.thinking_label.config(text=f"🧠 Analizando posibilidades{dots}")
                self.root.after(200, lambda: animate_thinking(count + 1))
            else:
                self.thinking_label.config(text="")
        
        animate_thinking()
    
    def check_and_continue(self):
        """Check game over and continue if needed"""
        if not self.check_game_over():
            self.switch_player()
            if self.game_mode == 'ai_vs_ai':
                self.root.after(1000, self.ai_move)
    
    # AI Algorithms
    def ai_random(self) -> Optional[Tuple[int, int]]:
        """Random AI - easiest level"""
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
        return random.choice(empty_cells) if empty_cells else None
    
    def ai_medium(self) -> Optional[Tuple[int, int]]:
        """Medium AI - blocks winning moves"""
        # Check for winning move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = self.current_player
                    if self.check_winner():
                        self.board[i][j] = ''
                        return (i, j)
                    self.board[i][j] = ''
        
        # Check for blocking move
        opponent = 'X' if self.current_player == 'O' else 'O'
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = opponent
                    if self.check_winner():
                        self.board[i][j] = ''
                        return (i, j)
                    self.board[i][j] = ''
        
        # Random move
        return self.ai_random()
    
    def ai_hard(self) -> Optional[Tuple[int, int]]:
        """Hard AI - strategic play"""
        # Priority: Win > Block > Center > Corner > Side
        
        # 1. Try to win
        move = self.find_winning_move(self.current_player)
        if move:
            return move
        
        # 2. Block opponent
        opponent = 'X' if self.current_player == 'O' else 'O'
        move = self.find_winning_move(opponent)
        if move:
            return move
        
        # 3. Take center
        if self.board[1][1] == '':
            return (1, 1)
        
        # 4. Take corners
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        empty_corners = [c for c in corners if self.board[c[0]][c[1]] == '']
        if empty_corners:
            return random.choice(empty_corners)
        
        # 5. Take sides
        return self.ai_random()
    
    def ai_minimax(self) -> Optional[Tuple[int, int]]:
        """Impossible AI - Minimax algorithm"""
        best_score = float('-inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = self.current_player
                    score = self.minimax(0, False)
                    self.board[i][j] = ''
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        return best_move
    
    def minimax(self, depth, is_maximizing):
        """Minimax algorithm implementation"""
        winner = self.check_winner()
        
        if winner == self.current_player:
            return 10 - depth
        elif winner == ('X' if self.current_player == 'O' else 'O'):
            return depth - 10
        elif self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '':
                        self.board[i][j] = self.current_player
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            opponent = 'X' if self.current_player == 'O' else 'O'
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '':
                        self.board[i][j] = opponent
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score
    
    def find_winning_move(self, player) -> Optional[Tuple[int, int]]:
        """Find winning move for a player"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = player
                    if self.check_winner() == player:
                        self.board[i][j] = ''
                        return (i, j)
                    self.board[i][j] = ''
        return None
    
    def switch_player(self):
        """Switch current player"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.update_status()
    
    def check_game_over(self):
        """Check if game is over"""
        winner = self.check_winner()
        if winner:
            self.game_over = True
            self.scores[winner] += 1
            self.highlight_winning_line()
            self.show_game_over_message(f"🎉 ¡{winner} ha ganado! 🎉")
            return True
        elif self.is_board_full():
            self.game_over = True
            self.scores['Draw'] += 1
            self.show_game_over_message("🤝 ¡Empate! 🤝")
            return True
        return False
    
    def check_winner(self):
        """Check for winner"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        
        return None
    
    def highlight_winning_line(self):
        """Highlight winning line with animation"""
        winner = self.check_winner()
        if not winner:
            return
        
        winning_positions = []
        
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == winner:
                winning_positions = [(i, 0), (i, 1), (i, 2)]
                break
        
        # Check columns
        if not winning_positions:
            for j in range(3):
                if self.board[0][j] == self.board[1][j] == self.board[2][j] == winner:
                    winning_positions = [(0, j), (1, j), (2, j)]
                    break
        
        # Check diagonals
        if not winning_positions:
            if self.board[0][0] == self.board[1][1] == self.board[2][2] == winner:
                winning_positions = [(0, 0), (1, 1), (2, 2)]
            elif self.board[0][2] == self.board[1][1] == self.board[2][0] == winner:
                winning_positions = [(0, 2), (1, 1), (2, 0)]
        
        # Animate winning line
        if winning_positions:
            def animate_win(step=0):
                if step < 10:
                    color = self.colors['accent'] if step % 2 == 0 else self.colors['primary']
                    for row, col in winning_positions:
                        self.buttons[row][col].config(bg=color)
                    self.root.after(200, lambda: animate_win(step + 1))
                else:
                    # Final color
                    for row, col in winning_positions:
                        self.buttons[row][col].config(bg=self.colors['primary'])
            
            animate_win()
    
    def is_board_full(self):
        """Check if board is full"""
        return all(self.board[i][j] != '' for i in range(3) for j in range(3))
    
    def show_game_over_message(self, message):
        """Show game over message"""
        messagebox.showinfo("¡Juego Terminado!", message)
        self.update_status()
    
    def new_game(self):
        """Start new game"""
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.move_count = 0
        self.thinking_label.config(text="")
        
        # Reset buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text='',
                    bg=self.colors['button_bg'],
                    state='normal',
                    relief='raised'
                )
        
        self.update_status()
        
        # If AI vs AI mode, start the game
        if self.game_mode == 'ai_vs_ai':
            self.root.after(1000, self.ai_move)
    
    def change_game_mode(self, mode):
        """Change game mode"""
        self.game_mode = mode
        self.new_game()
    
    def change_difficulty(self, difficulty):
        """Change AI difficulty"""
        self.difficulty = difficulty
        if difficulty == 'easy':
            self.thinking_time = 0.5
        elif difficulty == 'medium':
            self.thinking_time = 1.0
        elif difficulty == 'hard':
            self.thinking_time = 1.5
        else:  # impossible
            self.thinking_time = 2.0
    
    def show_stats(self):
        """Show detailed statistics"""
        total_games = sum(self.scores.values())
        if total_games == 0:
            messagebox.showinfo("📊 Estadísticas", "¡Aún no has jugado ninguna partida!")
            return
        
        x_percentage = (self.scores['X'] / total_games) * 100
        o_percentage = (self.scores['O'] / total_games) * 100
        draw_percentage = (self.scores['Draw'] / total_games) * 100
        
        stats_text = f"""
🎮 ESTADÍSTICAS DETALLADAS 🎮

📈 Partidas Totales: {total_games}

🏆 Victorias X: {self.scores['X']} ({x_percentage:.1f}%)
🏆 Victorias O: {self.scores['O']} ({o_percentage:.1f}%)
🤝 Empates: {self.scores['Draw']} ({draw_percentage:.1f}%)

🎯 Modo Actual: {self.game_mode}
🧠 Dificultad IA: {self.difficulty}

💪 ¡Sigue jugando para mejorar tus estadísticas!
        """
        
        messagebox.showinfo("📊 Estadísticas Completas", stats_text)
    
    def run(self):
        """Start the game"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🎮 Iniciando Tres en Raya BRUTAL...")
    print("🚀 Desarrollado por Edilson Ortiz")
    print("🤖 Con IA avanzada y algoritmo Minimax")
    print("=" * 50)
    
    game = AdvancedTicTacToe()
    game.run()
