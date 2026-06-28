import random

GRID_SIZE = 20  # Rejilla de 20x20
CELL_SIZE = 25  # Tamaño de cada celda

class SnakeGameLogic:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        """Reinicia todas las variables para una nueva partida."""
        self.snake = [(10, 10), (10, 11), (10, 12)]
        self.direction = "UP"
        self.game_over = False
        self.score = 0
        self.food = self.generate_food()

    def generate_food(self):
        """Genera comida en una posición aleatoria libre."""
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, new_direction):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def update_position(self):
        if self.game_over:
            return

        head_x, head_y = self.snake[0]

        if self.direction == "UP":
            head = (head_x, head_y - 1)
        elif self.direction == "DOWN":
            head = (head_x, head_y + 1)
        elif self.direction == "LEFT":
            head = (head_x - 1, head_y)
        elif self.direction == "RIGHT":
            head = (head_x + 1, head_y)

        # Colisiones con bordes
        if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
            self.game_over = True
            return

        # Colisión con el cuerpo
        if head in self.snake:
            self.game_over = True
            return

        # Movimiento y alimentación
        if head == self.food:
            self.snake.insert(0, head)
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.insert(0, head)
            self.snake.pop()