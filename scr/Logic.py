import random

# Constantes de la rejilla requeridas por main.py
GRID_SIZE = 20  # Número de celdas a lo ancho y alto
CELL_SIZE = 25  # Tamaño en píxeles de cada celda (puedes ajustarlo a tu gusto)

class SnakeGameLogic:
    def __init__(self):
        # Inicializa la serpiente en el centro de la rejilla (lista de tuplas [x, y])
        self.snake = [(10, 10), (10, 11), (10, 12)]
        self.direction = "UP"
        self.game_over = False
        self.food = self.generate_food()
        self.score = 0

    def generate_food(self):
        """Genera comida en una posición aleatoria que no colisione con la serpiente."""
        while True:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, new_direction):
        """Cambia la dirección impidiendo que se mueva en reversa directa."""
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def update_position(self):
        """Actualiza la posición de la serpiente y maneja las colisiones."""
        if self.game_over:
            return

        # Obtener la cabeza actual
        head_x, head_y = self.snake[0]

        # Calcular nueva posición según la dirección
        if self.direction == "UP":
            head = (head_x, head_y - 1)
        elif self.direction == "DOWN":
            head = (head_x, head_y + 1)
        elif self.direction == "LEFT":
            head = (head_x - 1, head_y)
        elif self.direction == "RIGHT":
            head = (head_x + 1, head_y)

        # 1. Colisión con los bordes de la rejilla
        if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
            self.game_over = True
            return

        # 2. Colisión con su propio cuerpo
        if head in self.snake:
            self.game_over = True
            return

        # 3. ¿Comió la manzana?
        if head == self.food:
            self.snake.insert(0, head)  # Inserta nueva cabeza
            self.score += 1
            self.food = self.generate_food()  # Nueva comida
        else:
            self.snake.insert(0, head)  # Inserta nueva cabeza
            self.snake.pop()  # Quita la cola para simular movimiento