import tkinter as tk
from tkinter import ttk, messagebox
from game import Mastermind, DIFFICULTIES
from logic import feedback


# Color palette for a polished game look
BG = "#1e1e2e"
CARD = "#2d2d44"
ACCENT = "#7aa2f7"
GREEN = "#9ece6a"
YELLOW = "#e0af68"
RED = "#f7768e"
TEXT = "#c0caf5"
DIM = "#565f89"
WHITE = "#ffffff"


class MastermindGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind - Code Breaker")
        self.root.geometry("700x650")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.game = None
        self.current_guess = []

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Game.TFrame", background=BG)
        self.style.configure("Card.TFrame", background=CARD)
        self.style.configure("Game.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 12))
        self.style.configure("Title.TLabel", background=BG, foreground=ACCENT, font=("Segoe UI", 28, "bold"))
        self.style.configure("Subtitle.TLabel", background=BG, foreground=DIM, font=("Segoe UI", 11))
        self.style.configure("Status.TLabel", background=CARD, foreground=WHITE, font=("Segoe UI", 13, "bold"))
        self.style.configure("Feedback.TLabel", background=CARD, foreground=WHITE, font=("Segoe UI", 16, "bold"))
        self.style.configure("History.Treeview", background=CARD, foreground=TEXT, fieldbackground=CARD, rowheight=28)
        self.style.configure("History.Treeview.Heading", background=CARD, foreground=WHITE, font=("Segoe UI", 11, "bold"))

        self.build_ui()
        self.start_new_game(difficulty="2")

    def build_ui(self):
        # Header
        header = ttk.Frame(self.root, style="Game.TFrame")
        header.pack(pady=15)
        ttk.Label(header, text="MASTERMIND", style="Title.TLabel").pack()
        ttk.Label(header, text="Crack the secret code", style="Subtitle.TLabel").pack()

        # Difficulty selection
        diff_frame = ttk.Frame(self.root, style="Game.TFrame")
        diff_frame.pack(pady=10)
        ttk.Label(diff_frame, text="Difficulty:", style="Game.TLabel").pack(side=tk.LEFT, padx=5)
        self.diff_var = tk.StringVar(value="2")
        for key, config in DIFFICULTIES.items():
            tk.Radiobutton(
                diff_frame,
                text=config["name"],
                variable=self.diff_var,
                value=key,
                command=self.on_difficulty_change,
                bg=BG,
                fg=TEXT,
                selectcolor=CARD,
                activebackground=BG,
                activeforeground=ACCENT,
                font=("Segoe UI", 11, "bold"),
            ).pack(side=tk.LEFT, padx=8)

        # Status card
        status_card = ttk.Frame(self.root, style="Card.TFrame", padding=15)
        status_card.pack(pady=10, padx=30, fill=tk.X)
        self.status_label = ttk.Label(status_card, text="", style="Status.TLabel")
        self.status_label.pack()

        # Secret code display
        self.code_frame = tk.Frame(self.root, bg=BG)
        self.code_frame.pack(pady=10)
        self.code_labels = []

        # Current guess display
        guess_card = ttk.Frame(self.root, style="Card.TFrame", padding=15)
        guess_card.pack(pady=10, padx=30, fill=tk.X)
        ttk.Label(guess_card, text="Your Guess", style="Subtitle.TLabel").pack()
        self.guess_display = ttk.Label(guess_card, text="_ _ _ _", style="Feedback.TLabel")
        self.guess_display.pack(pady=5)

        # Feedback display
        self.feedback_label = ttk.Label(guess_card, text="Enter your guess", style="Feedback.TLabel")
        self.feedback_label.pack()

        # Digit buttons
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=10)
        self.digit_buttons = {}
        for i in range(1, 9):
            btn = tk.Button(
                btn_frame,
                text=str(i),
                width=5,
                height=2,
                font=("Segoe UI", 14, "bold"),
                bg=CARD,
                fg=TEXT,
                activebackground=ACCENT,
                activeforeground=WHITE,
                command=lambda d=str(i): self.add_digit(d),
            )
            btn.grid(row=(i - 1) // 4, column=(i - 1) % 4, padx=8, pady=8)
            self.digit_buttons[str(i)] = btn

        # Control buttons
        ctrl_frame = tk.Frame(self.root, bg=BG)
        ctrl_frame.pack(pady=10)
        tk.Button(
            ctrl_frame,
            text="Clear",
            width=10,
            font=("Segoe UI", 12, "bold"),
            bg=DIM,
            fg=WHITE,
            command=self.clear_guess,
        ).pack(side=tk.LEFT, padx=10)
        self.submit_btn = tk.Button(
            ctrl_frame,
            text="Submit Guess",
            width=14,
            font=("Segoe UI", 12, "bold"),
            bg=ACCENT,
            fg=WHITE,
            command=self.submit_guess,
        )
        self.submit_btn.pack(side=tk.LEFT, padx=10)
        tk.Button(
            ctrl_frame,
            text="New Game",
            width=12,
            font=("Segoe UI", 12, "bold"),
            bg=GREEN,
            fg=BG,
            command=self.on_difficulty_change,
        ).pack(side=tk.LEFT, padx=10)

        # History table
        history_frame = ttk.Frame(self.root, style="Card.TFrame", padding=10)
        history_frame.pack(pady=15, padx=30, fill=tk.BOTH, expand=True)
        ttk.Label(history_frame, text="Guess History", style="Game.TLabel").pack(anchor="w", padx=5)

        columns = ("turn", "guess", "exact", "partial")
        self.tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
            height=8,
            style="History.Treeview",
        )
        self.tree.heading("turn", text="Turn")
        self.tree.heading("guess", text="Guess")
        self.tree.heading("exact", text="Exact")
        self.tree.heading("partial", text="Partial")
        self.tree.column("turn", width=80, anchor="center")
        self.tree.column("guess", width=150, anchor="center")
        self.tree.column("exact", width=100, anchor="center")
        self.tree.column("partial", width=100, anchor="center")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Result overlay label
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 18, "bold"),
            bg=BG,
            fg=WHITE,
        )
        self.result_label.pack(pady=10)

    def start_new_game(self, difficulty):
        self.game = Mastermind(difficulty=difficulty)
        cfg = DIFFICULTIES[difficulty]
        self.current_guess = []
        self.result_label.config(text="")

        self.status_label.config(
            text=f"Guess {cfg['length']} digits from 1-{cfg['symbols']} - {cfg['turns']} turns left"
        )
        self.feedback_label.config(text="Enter your guess", foreground=WHITE)
        self.update_guess_display()
        self.refresh_history()
        self.update_code_display(hidden=True)
        self.set_controls_enabled(True)
        self.update_digit_buttons()

    def on_difficulty_change(self):
        self.start_new_game(difficulty=self.diff_var.get())

    def update_digit_buttons(self):
        cfg = DIFFICULTIES[self.diff_var.get()]
        for digit, btn in self.digit_buttons.items():
            if int(digit) <= cfg["symbols"]:
                btn.config(state=tk.NORMAL, bg=CARD)
            else:
                btn.config(state=tk.DISABLED, bg=DIM)

    def add_digit(self, digit):
        if self.game.game_over:
            return
        if len(self.current_guess) < self.game.length:
            self.current_guess.append(digit)
            self.update_guess_display()

    def clear_guess(self):
        self.current_guess = []
        self.update_guess_display()

    def update_guess_display(self):
        cfg = DIFFICULTIES[self.diff_var.get()]
        display = " ".join(self.current_guess + ["_"] * (cfg["length"] - len(self.current_guess)))
        self.guess_display.config(text=display)

    def submit_guess(self):
        if self.game.game_over:
            return

        raw = "".join(self.current_guess)
        valid, error = self.game.validate_guess(raw)
        if not valid:
            messagebox.showwarning("Invalid guess", error)
            return

        guess = list(raw)
        exact, partial = feedback(self.game.code, guess)
        self.game.history.append((raw, exact, partial))
        self.game.turns -= 1

        self.feedback_label.config(
            text=f"Exact: {exact}   Partial: {partial}",
            foreground=GREEN if exact == self.game.length else YELLOW,
        )
        self.refresh_history()
        self.current_guess = []
        self.update_guess_display()

        cfg = DIFFICULTIES[self.diff_var.get()]
        self.status_label.config(
            text=f"Guess {cfg['length']} digits from 1-{cfg['symbols']} - {self.game.turns} turns left"
        )

        if exact == self.game.length:
            self.end_game(won=True)
        elif self.game.turns == 0:
            self.end_game(won=False)

    def refresh_history(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for turn, (guess, exact, partial) in enumerate(self.game.history, start=1):
            self.tree.insert("", tk.END, values=(turn, guess, exact, partial))

    def update_code_display(self, hidden=False):
        for widget in self.code_frame.winfo_children():
            widget.destroy()
        self.code_labels = []
        for i in range(self.game.length):
            text = "?" if hidden else self.game.code[i]
            lbl = tk.Label(
                self.code_frame,
                text=text,
                width=3,
                font=("Segoe UI", 20, "bold"),
                bg=CARD,
                fg=ACCENT if hidden else GREEN,
            )
            lbl.pack(side=tk.LEFT, padx=5)
            self.code_labels.append(lbl)

    def set_controls_enabled(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.submit_btn.config(state=state)
        for btn in self.digit_buttons.values():
            btn.config(state=state if enabled else tk.DISABLED)

    def end_game(self, won):
        self.game.game_over = True
        self.game.won = won
        self.set_controls_enabled(False)
        self.update_code_display(hidden=False)
        if won:
            self.result_label.config(text="You cracked the code!", fg=GREEN)
        else:
            code_str = "".join(self.game.code)
            self.result_label.config(text=f"You lost! The code was {code_str}", fg=RED)


if __name__ == "__main__":
    root = tk.Tk()
    app = MastermindGUI(root)
    root.mainloop()
