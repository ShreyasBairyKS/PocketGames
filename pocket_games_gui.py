import random
import tkinter as tk
from tkinter import ttk, messagebox

APP_TITLE = "PocketGames – GUI"
APP_MIN_W, APP_MIN_H = 880, 560

# -----------------------------
# Base: multi-screen framework
# -----------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(APP_MIN_W, APP_MIN_H)

        # Root container
        self.container = ttk.Frame(self, padding=16)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (Home, RPS, Hangman, HandCricket):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("Home")

        # styling
        style = ttk.Style(self)
        try:
            self.tk.call("tk", "scaling", 1.2)
        except Exception:
            pass
        style.configure("Card.TFrame", relief="raised", padding=14)
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("H2.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Body.TLabel", font=("Segoe UI", 11))
        style.configure("Accent.TButton", padding=8)
        style.configure("Danger.TButton", padding=8)
        style.map("Danger.TButton", foreground=[("active", "white")], background=[("active", "#d9534f")])

    def show(self, name: str):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

# -----------------------------
# Home screen
# -----------------------------
class Home(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = ttk.Label(self, text="PocketGames", style="Title.TLabel")
        subtitle = ttk.Label(
            self,
            text="Choose a game and have fun! (All local, no internet required)",
            style="Body.TLabel",
        )

        # Cards
        cards = ttk.Frame(self)
        rps = self._game_card(cards, "✊✋✌️  Rock–Paper–Scissors", "Play classic RPS vs computer.", lambda: controller.show("RPS"))
        hang = self._game_card(cards, "🔤 Hangman", "Guess the hidden word letter by letter.", lambda: controller.show("Hangman"))
        cricket = self._game_card(cards, "🏏 Hand Cricket", "Score runs without getting out!", lambda: controller.show("HandCricket"))

        title.pack(anchor="w")
        subtitle.pack(anchor="w", pady=(0, 12))
        cards.pack(fill="both", expand=True)

        # responsive grid
        for i, card in enumerate((rps, hang, cricket)):
            card.grid(row=0, column=i, sticky="nsew", padx=8, pady=8)
            cards.columnconfigure(i, weight=1)
        cards.rowconfigure(0, weight=1)

    def _game_card(self, parent, heading, desc, command):
        card = ttk.Frame(parent, style="Card.TFrame")
        ttk.Label(card, text=heading, style="H2.TLabel").pack(anchor="w")
        ttk.Label(card, text=desc, style="Body.TLabel", wraplength=240, justify="left").pack(anchor="w", pady=(6, 12))
        ttk.Button(card, text="Play", style="Accent.TButton", command=command).pack(anchor="e")
        return card

# -----------------------------
# Rock–Paper–Scissors
# -----------------------------
class RPS(ttk.Frame):
    CHOICES = ["Rock", "Paper", "Scissors"]
    RULES = {
        ("Rock", "Scissors"): "win",
        ("Paper", "Rock"): "win",
        ("Scissors", "Paper"): "win",
    }

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.player_score = 0
        self.computer_score = 0
        self.rounds = 0

        header = self._header("✊✋✌️ Rock–Paper–Scissors", lambda: controller.show("Home"))
        header.pack(fill="x", pady=(0, 10))

        scorebar = ttk.Frame(self)
        self.lbl_score = ttk.Label(scorebar, text=self._score_text(), style="H2.TLabel")
        self.lbl_score.pack(side="left")
        ttk.Button(scorebar, text="Reset", command=self.reset).pack(side="right")
        scorebar.pack(fill="x", pady=(0, 8))

        play = ttk.Frame(self)
        ttk.Label(play, text="Your move:", style="Body.TLabel").pack(anchor="w", pady=(0, 6))
        buttons = ttk.Frame(play)
        for c in self.CHOICES:
            ttk.Button(buttons, text=c, command=lambda x=c: self.play_round(x)).pack(side="left", padx=6)
        buttons.pack(anchor="w")
        self.status = ttk.Label(play, text="", style="Body.TLabel")
        self.status.pack(anchor="w", pady=(10, 0))
        play.pack(fill="both", expand=True)

    def _header(self, title, on_back):
        h = ttk.Frame(self)
        ttk.Button(h, text="← Back", command=on_back).pack(side="left")
        ttk.Label(h, text=title, style="Title.TLabel").pack(side="left", padx=10)
        return h

    def _score_text(self):
        return f"Score  You: {self.player_score}  |  Computer: {self.computer_score}  • Rounds: {self.rounds}"

    def reset(self):
        self.player_score = self.computer_score = self.rounds = 0
        self.lbl_score.config(text=self._score_text())
        self.status.config(text="")

    def play_round(self, player_choice):
        comp = random.choice(self.CHOICES)
        result = "draw"
        if player_choice != comp:
            result = "win" if (player_choice, comp) in self.RULES else "lose"

        self.rounds += 1
        if result == "win":
            self.player_score += 1
        elif result == "lose":
            self.computer_score += 1

        self.lbl_score.config(text=self._score_text())
        self.status.config(text=f"You chose {player_choice}, Computer chose {comp} → You {result.upper()}!")

    def on_show(self):
        pass

# -----------------------------
# Hangman
# -----------------------------
DEFAULT_WORDS = [
    "python", "java", "streamlit", "flask", "mongodb", "react", "algorithm",
    "database", "variable", "function", "package", "iterator", "compose",
]

class Hangman(ttk.Frame):
    MAX_TRIES = 7

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.word = ""
        self.progress = []
        self.guessed = set()
        self.tries_left = self.MAX_TRIES

        header = self._header("🔤 Hangman", lambda: controller.show("Home"))
        header.pack(fill="x", pady=(0, 10))

        # Top row: tries + word state
        top = ttk.Frame(self)
        self.lbl_tries = ttk.Label(top, text="", style="H2.TLabel")
        self.lbl_tries.pack(side="left")
        ttk.Button(top, text="New Word", command=self.new_word).pack(side="right")
        top.pack(fill="x", pady=(0, 10))

        # Word display
        word_card = ttk.Frame(self, style="Card.TFrame")
        self.lbl_word = ttk.Label(word_card, text="", font=("Consolas", 24, "bold"))
        self.lbl_word.pack(padx=10, pady=10)
        word_card.pack(fill="x", pady=(0, 10))

        # Guess controls
        controls = ttk.Frame(self)
        ttk.Label(controls, text="Enter a letter:", style="Body.TLabel").pack(side="left")
        self.entry = ttk.Entry(controls, width=6)
        self.entry.pack(side="left", padx=8)
        ttk.Button(controls, text="Guess", command=self.guess).pack(side="left")
        controls.pack(anchor="w", pady=(0, 6))

        self.lbl_guessed = ttk.Label(self, text="", style="Body.TLabel")
        self.lbl_guessed.pack(anchor="w")

        self.new_word()

    def _header(self, title, on_back):
        h = ttk.Frame(self)
        ttk.Button(h, text="← Back", command=on_back).pack(side="left")
        ttk.Label(h, text=title, style="Title.TLabel").pack(side="left", padx=10)
        return h

    def new_word(self):
        self.word = random.choice(DEFAULT_WORDS)
        self.progress = ["_" for _ in self.word]
        self.guessed = set()
        self.tries_left = self.MAX_TRIES
        self._refresh_labels()

    def _refresh_labels(self):
        self.lbl_tries.config(text=f"Tries left: {self.tries_left}")
        self.lbl_word.config(text=" ".join(self.progress))
        if self.guessed:
            self.lbl_guessed.config(text=f"Guessed: {', '.join(sorted(self.guessed))}")
        else:
            self.lbl_guessed.config(text="")

    def guess(self):
        val = self.entry.get().strip().lower()
        self.entry.delete(0, tk.END)
        if not val or not val.isalpha() or len(val) != 1:
            messagebox.showinfo("Hangman", "Please enter a single letter.")
            return
        if val in self.guessed:
            messagebox.showinfo("Hangman", "Already guessed that letter.")
            return
        self.guessed.add(val)

        if val in self.word:
            for i, ch in enumerate(self.word):
                if ch == val:
                    self.progress[i] = val
        else:
            self.tries_left -= 1

        self._refresh_labels()
        if "_" not in self.progress:
            messagebox.showinfo("Hangman", f"You won! The word was '{self.word}'.")
            self.new_word()
        elif self.tries_left <= 0:
            messagebox.showinfo("Hangman", f"Out of tries! The word was '{self.word}'.")
            self.new_word()

    def on_show(self):
        self.entry.focus_set()

# -----------------------------
# Hand Cricket (1–6)
# -----------------------------
class HandCricket(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header = self._header("🏏 Hand Cricket", lambda: controller.show("Home"))
        header.pack(fill="x", pady=(0, 10))

        body = ttk.Frame(self)
        # Score / phase
        self.lbl_info = ttk.Label(body, text="", style="H2.TLabel")
        self.lbl_info.grid(row=0, column=0, sticky="w")

        # Buttons 1–6
        self.buttons = ttk.Frame(body)
        ttk.Label(self.buttons, text="Choose your run (1–6):", style="Body.TLabel").pack(anchor="w", pady=(0, 6))
        for n in range(1, 7):
            ttk.Button(self.buttons, text=str(n), command=lambda x=n: self.play_ball(x)).pack(side="left", padx=4)
        self.buttons.grid(row=1, column=0, sticky="w", pady=(10, 0))

        # Log
        log_card = ttk.Frame(body, style="Card.TFrame")
        ttk.Label(log_card, text="Commentary", style="H2.TLabel").pack(anchor="w")
        self.txt = tk.Text(log_card, height=16, wrap="word")
        self.txt.pack(fill="both", expand=True, pady=(8, 0))
        log_card.grid(row=2, column=0, sticky="nsew", pady=(12, 0))

        # Reset
        ttk.Button(body, text="New Match", command=self.new_match).grid(row=3, column=0, pady=10, sticky="w")

        body.columnconfigure(0, weight=1)
        body.rowconfigure(2, weight=1)
        body.pack(fill="both", expand=True)

        # State
        self.new_match()

    def _header(self, title, on_back):
        h = ttk.Frame(self)
        ttk.Button(h, text="← Back", command=on_back).pack(side="left")
        ttk.Label(h, text=title, style="Title.TLabel").pack(side="left", padx=10)
        return h

    def new_match(self):
        self.phase = "player_batting"   # then "computer_batting", then "done"
        self.player_score = 0
        self.computer_score = 0
        self.player_out = False
        self.computer_out = False
        self.target = None
        self.txt.delete("1.0", tk.END)
        self._set_info("You are batting first. Score as much as you can!")
        self._log("New match started. You bat first.")

    def _set_info(self, text):
        self.lbl_info.config(text=text)

    def _log(self, line):
        self.txt.insert(tk.END, "• " + line + "\n")
        self.txt.see(tk.END)

    def play_ball(self, player_num):
        if self.phase == "done":
            messagebox.showinfo("Match over", "Start a new match.")
            return

        comp_num = random.randint(1, 6)

        if self.phase == "player_batting":
            if player_num == comp_num:
                self.player_out = True
                self._log(f"PLAYER chose {player_num}, COMP chose {comp_num} → OUT! Final: {self.player_score}")
                self.target = self.player_score + 1
                self.phase = "computer_batting"
                self._set_info(f"Computer batting. Target: {self.target}")
            else:
                self.player_score += player_num
                self._log(f"PLAYER {player_num} vs COMP {comp_num} → runs added. Score: {self.player_score}")
        elif self.phase == "computer_batting":
            if player_num == comp_num:
                self.computer_out = True
                self._log(f"PLAYER chose {player_num}, COMP {comp_num} → COMPUTER OUT! Final: {self.computer_score}")
                # Decide result
                self._end_match()
            else:
                self.computer_score += comp_num
                self._log(f"PLAYER {player_num} vs COMP {comp_num} → computer scores {comp_num}. Total: {self.computer_score}")
                if self.computer_score >= self.target:
                    self._log("Computer reached the target!")
                    self._end_match()

        # Update title
        if self.phase == "player_batting":
            self._set_info(f"Your score: {self.player_score}")
        elif self.phase == "computer_batting":
            self._set_info(f"Computer chasing {self.target} • Score: {self.computer_score}")

    def _end_match(self):
        self.phase = "done"
        if self.computer_score >= (self.player_score + 1):
            msg = f"Computer won by {self.computer_score - self.player_score} run(s)."
        elif self.computer_score == self.player_score:
            msg = "Match tied."
        else:
            msg = f"You won by {self.player_score - self.computer_score} run(s)."
        self._log("Result: " + msg)
        messagebox.showinfo("Result", msg)

# -----------------------------
# Launch
# -----------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
