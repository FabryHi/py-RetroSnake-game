# Punto de entrada principal del juego.
import flet as ft
import asyncio
from Logic import SnakeGameLogic, GRID_SIZE, CELL_SIZE

def main(page: ft.Page):
    # Configuraciones principales de la ventana
    page.title = "RetroSnake-Game"
    page.window_width = GRID_SIZE * CELL_SIZE + 40
    page.window_height = GRID_SIZE * CELL_SIZE + 100
    page.window_resizable = False
    
    # IMPORTANTE: Usamos 'Colors' con C mayúscula para tu versión de Flet
    page.bgcolor = ft.Colors.BLACK 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Inicializamos la lógica del juego
    game = SnakeGameLogic()

    # Elemento visual para el puntaje
    score_text = ft.Text(value=f"Score: {game.score}", size=24, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)

    # El contenedor del tablero de juego donde se dibujará la serpiente
    game_board = ft.Stack(
        width=GRID_SIZE * CELL_SIZE,
        height=GRID_SIZE * CELL_SIZE,
    )

    def draw_board():
        """Limpia el tablero y redibuja la serpiente y la comida."""
        game_board.controls.clear()

        # 1. Dibujar el fondo del tablero para delimitar los bordes
        game_board.controls.append(
            ft.Container(
                width=GRID_SIZE * CELL_SIZE,
                height=GRID_SIZE * CELL_SIZE,
                bgcolor=ft.Colors.GREY_900,
                border_radius=5
            )
        )

        # 2. Dibujar la comida (Manzana)
        food_x, food_y = game.food
        game_board.controls.append(
            ft.Container(
                width=CELL_SIZE - 2,
                height=CELL_SIZE - 2,
                bgcolor=ft.Colors.RED,
                border_radius=CELL_SIZE // 2,  # Hacerla redonda
                left=food_x * CELL_SIZE + 1,
                top=food_y * CELL_SIZE + 1,
            )
        )

        # 3. Dibujar la serpiente
        for i, (x, y) in enumerate(game.snake):
            # La cabeza tiene un color ligeramente diferente al cuerpo
            color = ft.Colors.GREEN_ACCENT_400 if i == 0 else ft.Colors.GREEN_700
            game_board.controls.append(
                ft.Container(
                    width=CELL_SIZE - 2,
                    height=CELL_SIZE - 2,
                    bgcolor=color,
                    border_radius=4,
                    left=x * CELL_SIZE + 1,
                    top=y * CELL_SIZE + 1,
                )
            )
        
        # Actualizar el texto del puntaje
        score_text.value = f"Score: {game.score}"
        page.update()

    def on_keyboard_event(e: ft.KeyboardEvent):
        """Maneja los cambios de dirección con las flechas del teclado o WASD."""
        if e.key == "Arrow Up" or e.key.upper() == "W":
            game.change_direction("UP")
        elif e.key == "Arrow Down" or e.key.upper() == "S":
            game.change_direction("DOWN")
        elif e.key == "Arrow Left" or e.key.upper() == "A":
            game.change_direction("LEFT")
        elif e.key == "Arrow Right" or e.key.upper() == "D":
            game.change_direction("RIGHT")

    # Registrar el evento del teclado en la página
    page.on_keyboard_event = on_keyboard_event

    # Agregar los componentes visuales a la pantalla
    page.add(
        ft.Column(
            controls=[
                score_text,
                game_board
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    async def game_loop():
        """Bucle principal asíncrono que corre el juego y maneja el Game Over."""
        while not game.game_over:
            game.update_position()
            draw_board()
            # Controla la velocidad del juego (0.15 segundos por movimiento)
            await asyncio.sleep(0.15)
        
        # Pantalla de Game Over
        game_board.controls.append(
            ft.Container(
                content=ft.Text("GAME OVER", size=40, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
                width=GRID_SIZE * CELL_SIZE,
                height=GRID_SIZE * CELL_SIZE,
            )
        )
        page.update()

    # Dibujar el estado inicial e iniciar el juego asíncronamente
    draw_board()
    page.run_task(game_loop)

# Lanzamiento de la aplicación nativa
if __name__ == "__main__":
    ft.app(target=main)