# Interfaz gráfica (ventanas, botones, renderizado de la serpiente)
import flet as ft

CELL_SIZE = 20

def create_board_elements(game_stack: ft.Stack, logic):
    """Estructura repetitiva para dibujar los elementos en base a la lógica actual."""
    game_stack.controls.clear()

    # 1. Dibujar la comida (Cuadrado rojo)
    game_stack.controls.append(
        ft.Container(
            width=CELL_SIZE,
            height=CELL_SIZE,
            bgcolor=ft.colors.RED_ACCENT,
            border_radius=5,
            left=logic.food[0] * CELL_SIZE,
            top=logic.food[1] * CELL_SIZE,
        )
    )

    # 2. Dibujar la serpiente (Verde, cabeza más clara)
    for i, segment in enumerate(logic.snake):
        color = ft.colors.GREEN_100 if i == 0 else ft.colors.GREEN_700
        game_stack.controls.append(
            ft.Container(
                width=CELL_SIZE - 2,
                height=CELL_SIZE - 2,
                bgcolor=color,
                border_radius=4,
                left=segment[0] * CELL_SIZE,
                top=segment[1] * CELL_SIZE,
            )
        )