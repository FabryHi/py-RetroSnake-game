# Punto de entrada principal del juego.
import flet as ft

def main(page: ft.Page):
    # 1. Configuración básica de la ventana
    page.title = "Snake Game - RaymiOS"
    page.window_width = 450
    page.window_height = 550
    page.window_resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 2. Componentes visuales básicos
    score_text = ft.Text("Puntuación: 0", size=20, weight=ft.FontWeight.BOLD)
    
    # Tablero de juego (Cuadrícula de 400x400)
    game_board = ft.Container(
        width=400,
        height=400,
        bgcolor=ft.colors.BLACK,
        border=ft.border.all(2, ft.colors.GREEN_ACCENT)
    )

    # 3. Dibujar los elementos en la pantalla
    page.add(
        score_text,
        ft.Divider(height=10, color=ft.colors.TRANSPARENT),
        game_board
    )

if __name__ == "__main__":
    ft.app(target=main)