# RetroSnake-Game   -   Logica de Programación

## Integrantes
* Fabricio Jonathan Hidalgo Eras

## Objetivo del sistema
Desarrollar una versión moderna y multiplataforma del clásico juego de la serpiente (Snake) utilizando Python y el framework Flet. El sistema está diseñado para ejecutarse de manera nativa en entornos de escritorio, navegadores web y dispositivos móviles, ofreciendo una experiencia interactiva fluida con controles adaptativos.

## Descripción de funcionalidades
* **Movimiento Direccional:** Control de la serpiente mediante teclado físico (para PC) y un D-Pad táctil integrado en la interfaz gráfica (para móviles).
*
* **Sistema de Dificultad:** Selector de niveles (Fácil, Medio, Difícil) que ajusta dinámicamente la velocidad del ciclo de juego.
* 
* **Gestión de Puntuación:** Seguimiento en tiempo real de la puntuación actual y almacenamiento del récord máximo (High Score) durante la sesión activa.
*
* **Detección de Colisiones:** Lógica de validación que detecta impactos contra los límites del tablero o el propio cuerpo de la serpiente, activando el estado de "Game Over".
*
* **Control de Flujo de Partida:** Botones dinámicos que permiten iniciar (Play) y reiniciar (Restart) la partida en cualquier momento sin cerrar la aplicación.

## Fecha
Junio de 2026

---

## Instalación y Ejecución

Sigue estos pasos en tu terminal (PowerShell o CMD) para configurar el entorno y ejecutar el juego localmente:

### 1. Crear el entorno virtual (venv)
Asegúrate de estar en la carpeta principal de tu proyecto y ejecuta el siguiente comando para crear un entorno aislado:

bash
        python -m venv venv
        activamos el entorno
        venv\Scripts\Activate.ps1
        
** comando para que cualquiera lo utilice (pip install -r requirements.txt) **

### 2. Ejecutamos con 

------flet run scr/main.py o (flet run --web scr/main.py)--- en Windows


