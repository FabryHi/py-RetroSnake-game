# Punto de entrada principal del juego.
import flet as ft
import asyncio
from Logic import SnakeGameLogic, GRID_SIZE, CELL_SIZE

def main(page: ft.Page):
    # Configuraciones principales de la ventana (Escritorio)
    page.title = "RetroSnake-Game"
    page.window_width = GRID_SIZE * CELL_SIZE + 60
    page.window_height = GRID_SIZE * CELL_SIZE + 400 # Ampliado para dar espacio a los controles táctiles
    page.window_resizable = False
    
    # Ajustes universales (Web/Móvil)
    page.bgcolor = ft.Colors.BLACK 
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO # Evita que se corte la app en pantallas pequeñas de móvil

    # Variables de estado del juego
    game = [SnakeGameLogic()] 
    is_playing = [False]
    high_score = [0] 

    # --- 1. HEADER (Puntuación actual, Récord y Dificultad) ---
    score_text = ft.Text(value="Score: 0 | Récord: 0", size=18, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    
    difficulty_dropdown = ft.Dropdown(
        value="Medio",
        options=[
            ft.dropdown.Option("Fácil"),
            ft.dropdown.Option("Medio"),
            ft.dropdown.Option("Difícil"),
        ],
        width=110,
        text_size=14,
        bgcolor=ft.Colors.GREY_900,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.GREY_700
    )

    header = ft.Row(
        controls=[score_text, difficulty_dropdown],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        width=GRID_SIZE * CELL_SIZE
    )

    # --- 2. BODY (Tablero de Juego) ---
    game_board = ft.Stack(
        width=GRID_SIZE * CELL_SIZE,
        height=GRID_SIZE * CELL_SIZE,
    )

    # --- 3. FOOTER (Botones Play y Restart) ---
    play_button = ft.Button(
        content="Play Game",
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_700,
    )
    
    restart_button = ft.Button(
        content="Restart",
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_700,
        disabled=True
    )

    footer = ft.Row(
        controls=[play_button, restart_button],
        alignment=ft.MainAxisAlignment.CENTER,
        width=GRID_SIZE * CELL_SIZE,
        spacing=20 
    )

    # --- 4. CONTROLES MÓVILES (D-Pad Táctil) ---
    def btn_up(e):
        if is_playing[0] and not game[0].game_over: game[0].change_direction("UP")
    def btn_down(e):
        if is_playing[0] and not game[0].game_over: game[0].change_direction("DOWN")
    def btn_left(e):
        if is_playing[0] and not game[0].game_over: game[0].change_direction("LEFT")
    def btn_right(e):
        if is_playing[0] and not game[0].game_over: game[0].change_direction("RIGHT")

    mobile_controls = ft.Column(
        controls=[
            ft.Row([
                ft.Button(content="▲", on_click=btn_up, color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_800)
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Row([
                ft.Button(content="◄", on_click=btn_left, color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_800),
                ft.Container(width=10), # Espacio central pequeño
                ft.Button(content="►", on_click=btn_right, color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_800),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Row([
                ft.Button(content="▼", on_click=btn_down, color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_800)
            ], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=5 # Espacio vertical entre los botones
    )

    # Función para determinar la velocidad según la dificultad
    def get_speed():
        speeds = {"Fácil": 0.25, "Medio": 0.15, "Difícil": 0.08}
        return speeds.get(difficulty_dropdown.value, 0.15)

    def draw_board():
        """Limpia el tablero y redibuja la serpiente y la comida."""
        game_board.controls.clear()

        # Fondo del tablero
        game_board.controls.append(
            ft.Container(
                width=GRID_SIZE * CELL_SIZE,
                height=GRID_SIZE * CELL_SIZE,
                bgcolor=ft.Colors.GREY_900,
                border_radius=5
            )
        )

        # Comida 
        food_x, food_y = game[0].food
        game_board.controls.append(
            ft.Container(
                # NOTA: Si vas a usar la imagen de la manzana en PNG, comenta la línea 'bgcolor' 
                # y descomenta el bloque 'content=ft.Image(...)'
                bgcolor=ft.Colors.RED,
                # content=ft.Image(src="manzana.png", fit=ft.ImageFit.CONTAIN),
                width=CELL_SIZE - 2,
                height=CELL_SIZE - 2,
                border_radius=CELL_SIZE // 2,
                left=food_x * CELL_SIZE + 1,
                top=food_y * CELL_SIZE + 1,
            )
        )

        # Serpiente
        for i, (x, y) in enumerate(game[0].snake):
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
        
        # Pantalla de Game Over
        if game[0].game_over:
            game_board.controls.append(
                ft.Container(
                    content=ft.Text("GAME OVER", size=40, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLACK),
                    width=GRID_SIZE * CELL_SIZE,
                    height=GRID_SIZE * CELL_SIZE,
                )
            )

        # Comprobar y actualizar el puntaje más alto (Récord)
        if game[0].score > high_score[0]:
            high_score[0] = game[0].score

        # Actualizar la etiqueta del texto
        score_text.value = f"Score: {game[0].score} | Récord: {high_score[0]}"
        page.update()

    async def game_loop():
        """Bucle principal asíncrono."""
        while is_playing[0] and not game[0].game_over:
            game[0].update_position()
            draw_board()
            await asyncio.sleep(get_speed())
        
        if game[0].game_over:
            is_playing[0] = False
            difficulty_dropdown.disabled = False
            draw_board()
            page.update()

    def start_game(e):
        if not is_playing[0]:
            is_playing[0] = True
            play_button.disabled = True
            restart_button.disabled = False
            difficulty_dropdown.disabled = True 
            page.update()
            page.run_task(game_loop)

    def restart_game(e):
        game[0] = SnakeGameLogic() 
        difficulty_dropdown.disabled = True
        play_button.disabled = True
        restart_button.disabled = False
        
        if not is_playing[0]:
            is_playing[0] = True
            page.run_task(game_loop)
            
        page.update()

    play_button.on_click = start_game
    restart_button.on_click = restart_game

    def on_keyboard_event(e: ft.KeyboardEvent):
        """Soporte para teclado (Escritorio/Web)"""
        if not is_playing[0] or game[0].game_over:
            return
            
        if e.key == "Arrow Up" or e.key.upper() == "W":
            game[0].change_direction("UP")
        elif e.key == "Arrow Down" or e.key.upper() == "S":
            game[0].change_direction("DOWN")
        elif e.key == "Arrow Left" or e.key.upper() == "A":
            game[0].change_direction("LEFT")
        elif e.key == "Arrow Right" or e.key.upper() == "D":
            game[0].change_direction("RIGHT")

    page.on_keyboard_event = on_keyboard_event

    # Estructura final de la UI (Agregamos el D-Pad al final)
    page.add(
        ft.Column(
            controls=[
                header,
                ft.Container(height=5), 
                game_board,
                ft.Container(height=5), 
                footer,
                ft.Container(height=15), # Espaciador antes del pad
                mobile_controls # D-Pad Táctil
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    draw_board()

if __name__ == "__main__":
    ft.run(main)