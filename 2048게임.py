import tkinter as tk
import random
import time

class Game2048(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.master.title("2048 Game")
        self.main_grid = tk.Frame(self, bg="azure3", bd=3, width=400, height=400)
        self.main_grid.grid(pady=(100, 0))
        self.make_GUI()
        self.start_game()
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

    def make_GUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg="azure4",
                    width=100,
                    height=100
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg="azure4")
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # Score label
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=40, anchor="center")
        tk.Label(
            score_frame,
            text="Score",
            font=("Helvetica", 24)
        ).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=("Helvetica", 48))
        self.score_label.grid(row=1)

    def start_game(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        self.add_new_tile()
        self.add_new_tile()
        self.score = 0
        self.update_GUI()

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]
        self.score_label.configure(text=str(self.score))

    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    def add_new_tile(self):
        if random.random() < 0.9:
            value = 2
        else:
            value = 4
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while self.matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = value

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg="azure4")
                    self.cells[i][j]["number"].configure(bg="azure4", text="")
                else:
                    self.cells[i][j]["frame"].configure(bg="light sea green")
                    self.cells[i][j]["number"].configure(
                        bg="light sea green",
                        fg="white",
                        font=("Helvetica", 55, "bold"),
                        text=str(cell_value)
                    )
        self.update_idletasks()

    def animate(self, direction):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value != 0:
                    self.cells[i][j]["number"].configure(
                        fg="green",
                        font=("Helvetica", 55, "bold")
                    )
        self.update_idletasks()
        time.sleep(0.2)
        self.update_GUI()
        time.sleep(0.2)

        if direction == "left":
            self.stack()
            self.combine()
            self.stack()
        elif direction == "right":
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
        elif direction == "up":
            self.transpose()
            self.stack()
            self.combine()
            self.stack()
            self.transpose()
        elif direction == "down":
            self.transpose()
            self.reverse()
            self.stack()
            self.combine()
            self.stack()
            self.reverse()
            self.transpose()

        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def left(self, event):
        self.animate("left")

    def right(self, event):
        self.animate("right")

    def up(self, event):
        self.animate("up")

    def down(self, event):
        self.animate("down")

    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You win!",
                bg="green",
                fg="white",
                font=("Helvetica", 48, "bold")
            ).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game over!",
                bg="red",
                fg="white",
                font=("Helvetica", 48, "bold")
            ).pack()

def main():
    game = Game2048()
    game.mainloop()

if __name__ == "__main__":
    main()