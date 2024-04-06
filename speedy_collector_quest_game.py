import tkinter as tk
import random

# Global variables
WIDTH = 600  # Adjusted width
HEIGHT = 400  # Adjusted height
CHARACTER_SIZE = 20
ITEM_SIZE = 15
CHARACTER_SPEED = 10
ITEM_SPEED = 5
ITEMS_TO_COLLECT = 20

class Game:
    def __init__(self, master):
        self.master = master
        self.master.title("Speedy Collector Quest")

        # Canvas
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()

        # Character
        self.character = self.canvas.create_rectangle(
            50, HEIGHT//2, 50 + CHARACTER_SIZE, HEIGHT//2 + CHARACTER_SIZE, fill="blue"
        )

        # Items
        self.items = []
        self.generate_items()

        # Obstacles
        self.obstacles = []
        self.generate_obstacles()

        # Game controls
        self.collectible_items = ITEMS_TO_COLLECT
        self.score = 0
        self.score_label = tk.Label(master, text=f"Score: {self.score}", bg="white")
        self.score_label.pack()

        self.speed_scale = tk.Scale(master, from_=1, to=10, orient=tk.HORIZONTAL, label="Game Speed", length=200)
        self.speed_scale.set(5)  # Default speed
        self.speed_scale.pack()

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_game)
        self.pause_button.pack()

        self.restart_button = tk.Button(master, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        # Game state
        self.game_paused = False
        self.speed = self.speed_scale.get()

        self.canvas.bind("<KeyPress>", self.move_character)
        self.canvas.focus_set()
        self.move_items()

    def generate_items(self):
        for _ in range(ITEMS_TO_COLLECT):
            x = random.randint(50, WIDTH - ITEM_SIZE)
            y = random.randint(50, HEIGHT - ITEM_SIZE)
            item = self.canvas.create_rectangle(
                x, y, x + ITEM_SIZE, y + ITEM_SIZE, fill="green"
            )
            self.items.append(item)

    def generate_obstacles(self):
        for _ in range(5):
            x = random.randint(50, WIDTH - ITEM_SIZE)
            y = random.randint(50, HEIGHT - ITEM_SIZE)
            obstacle = self.canvas.create_rectangle(
                x, y, x + ITEM_SIZE, y + ITEM_SIZE, fill="red"
            )
            self.obstacles.append(obstacle)

    def move_character(self, event):
        key = event.keysym
        x1, y1, x2, y2 = self.canvas.coords(self.character)

        if key == "Up" and y1 > 0:
            self.canvas.move(self.character, 0, -CHARACTER_SPEED)
        elif key == "Down" and y2 < HEIGHT:
            self.canvas.move(self.character, 0, CHARACTER_SPEED)
        elif key == "Left" and x1 > 0:
            self.canvas.move(self.character, -CHARACTER_SPEED, 0)
        elif key == "Right" and x2 < WIDTH:
            self.canvas.move(self.character, CHARACTER_SPEED, 0)

        self.check_collision()

    def move_items(self):
        if not self.game_paused:
            for item in self.items:
                self.canvas.move(item, -ITEM_SPEED, 0)
                x1, _, x2, _ = self.canvas.coords(item)
                if x2 < 0:
                    self.canvas.move(item, WIDTH + ITEM_SIZE, 0)
            for obstacle in self.obstacles:
                self.canvas.move(obstacle, -ITEM_SPEED, 0)
                x1, _, x2, _ = self.canvas.coords(obstacle)
                if x2 < 0:
                    self.canvas.move(obstacle, WIDTH + ITEM_SIZE, 0)
            self.canvas.after(self.speed, self.move_items)

    def check_collision(self):
        character_coords = self.canvas.coords(self.character)
        for item in self.items[:]:
            item_coords = self.canvas.coords(item)
            if self.is_collision(character_coords, item_coords):
                self.canvas.delete(item)
                self.items.remove(item)
                self.collectible_items -= 1
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
                if self.collectible_items == 0:
                    self.game_over("Congratulations! You collected all items.")
        for obstacle in self.obstacles[:]:
            obstacle_coords = self.canvas.coords(obstacle)
            if self.is_collision(character_coords, obstacle_coords):
                self.game_over("Game Over! You hit an obstacle.")

    def is_collision(self, coords1, coords2):
        x1, y1, x2, y2 = coords1
        x3, y3, x4, y4 = coords2
        return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

    def game_over(self, message):
        self.canvas.delete("all")
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text=message, font=("Helvetica", 30), fill="red")

    def pause_game(self):
        self.game_paused = not self.game_paused
        if self.game_paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")
            self.move_items()

    def restart_game(self):
        self.canvas.delete("all")
        self.character = self.canvas.create_rectangle(
            50, HEIGHT//2, 50 + CHARACTER_SIZE, HEIGHT//2 + CHARACTER_SIZE, fill="blue"
        )
        self.items = []
        self.generate_items()
        self.obstacles = []
        self.generate_obstacles()
        self.collectible_items = ITEMS_TO_COLLECT
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.game_paused = False
        self.pause_button.config(text="Pause")
        self.move_items()

def main():
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

if __name__ == "__main__":
    main()
