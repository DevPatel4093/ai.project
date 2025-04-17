import json
import time
import tkinter as tk
from tkinter import messagebox, filedialog


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Sudoku Solver")
        self.root.configure(bg="white")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.steps = []
        self.step_index = 0
        self.selected_cell = None
        self.start_time = time.time()
        self.timer_label = None
        self.create_widgets()
        self.update_timer()

    def create_widgets(self):
        # Title and Timer
        title_frame = tk.Frame(self.root, bg="white")
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame, text="Sudoku", font=("Georgia", 24, "bold"),
            bg="white", fg="#1e1e1e"
        )
        title_label.pack(side=tk.TOP, pady=10)

        self.timer_label = tk.Label(
            title_frame, text="Time: 0s", font=("Arial", 10),
            bg="white", fg="black"
        )
        self.timer_label.pack(side=tk.RIGHT, padx=20)

        # Sudoku grid
        container = tk.Frame(self.root, bg="white")
        container.pack(expand=True)

        grid_frame = tk.Frame(container, bg="#1e1e1e", padx=10, pady=10)
        grid_frame.grid(row=0, column=0)

        for i in range(9):
            for j in range(9):
                entry = tk.Entry(
                    grid_frame, width=3, font=('Consolas', 18),
                    justify='center', bg="#2e2e2e", fg="white",
                    insertbackground="white", highlightthickness=1,
                    highlightbackground="#555"
                )
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.bind("<Button-1>", lambda e, row=i, col=j: self.select_cell(row, col))
                self.entries[i][j] = entry
                self.create_tooltip(entry, f"Cell ({i+1},{j+1})")

        # Button panel
        button_frame = tk.Frame(container, bg="white")
        button_frame.grid(row=2, column=0, pady=20)

        button_config = {
            "bg": "#444", "fg": "white", "font": ("Times New Roman", 12, "bold"),
            "activebackground": "#666", "width": 12, "height": 1
        }

        buttons = [
            ("Solve Next", self.solve_next, "Solve next step"),
            ("Clear", self.clear_board, "Clear the board"),
            ("Sample Puzzle", self.load_sample, "Load a sample puzzle"),
            ("Save Puzzle", self.save_to_file, "Save current puzzle"),
            ("Load Puzzle", self.load_from_file, "Load puzzle from file")
        ]

        for idx, (text, cmd, tip) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=cmd, **button_config)
            btn.grid(row=0, column=idx, padx=5)
            self.add_hover_effect(btn, "#555", "#444")
            self.create_tooltip(btn, tip)

    def add_hover_effect(self, widget, hover_color, default_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=default_color))

    def create_tooltip(self, widget, text):
        def on_enter(e):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.geometry(f"+{e.x_root + 10}+{e.y_root + 10}")
            label = tk.Label(tooltip, text=text, bg="yellow", relief="solid", borderwidth=1)
            label.pack()
            widget.tooltip = tooltip

        def on_leave(e):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed}s")
        self.root.after(1000, self.update_timer)

    def select_cell(self, row, col):
        if self.selected_cell:
            self.entries[self.selected_cell[0]][self.selected_cell[1]].config(highlightbackground="#555")
        self.selected_cell = (row, col)
        self.entries[row][col].config(highlightbackground="red")

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(bg="#2e2e2e")
        self.steps = []
        self.step_index = 0

    def load_sample(self):
        sample = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.set_board(sample)
        self.steps = []
        self.step_index = 0

    def save_to_file(self):
        board = self.get_board()
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(board, f)
            messagebox.showinfo("Saved", "Puzzle saved successfully!")

    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                board = json.load(f)
            self.set_board(board)
            self.steps = []
            self.step_index = 0

    def solve_next(self):
        if not self.steps:
            self.board = self.get_board()
            self.steps = []
            self.step_index = 0
            self.solve_with_steps(self.board.copy())

        if self.step_index < len(self.steps):
            row, col, num = self.steps[self.step_index]
            self.entries[row][col].delete(0, tk.END)
            self.entries[row][col].insert(0, str(num))
            self.entries[row][col].config(bg="#5cb85c")
            self.root.after(300, lambda: self.entries[row][col].config(bg="#2e2e2e"))
            self.board[row][col] = num
            self.step_index += 1
        else:
            messagebox.showinfo("Completed", "Sudoku solved!")

    def is_valid(self, board, row, col, num):
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def solve_with_steps(self, board):
        def backtrack():
            empty = self.find_empty(board)
            if not empty:
                return True
            row, col = empty
            for num in range(1, 10):
                if self.is_valid(board, row, col, num):
                    board[row][col] = num
                    self.steps.append((row, col, num))
                    if backtrack():
                        return True
                    board[row][col] = 0
                    self.steps.pop()
            return False

        backtrack()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x750")
    app = SudokuGUI(root)
    root.mainloop()