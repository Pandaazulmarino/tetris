import pygame
import random
import time 

ANCHO_TABLERO, ALTO_TABLERO = 10, 20
TAMANO_CELDA = 30
ANCHO_PANTALLA = ANCHO_TABLERO * TAMANO_CELDA
ALTO_PANTALLA = ALTO_TABLERO * TAMANO_CELDA
COLOR_FONDO = (0, 0, 0)      # Negro
COLOR_LINEA = (50, 50, 50)   # Gris para las líneas de la cuadrícula
COLOR_SOMBRA = (200, 200, 200)  # Gris claro para la sombra

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Tetris")
fuente = pygame.font.SysFont(None, 48) 

PIEZAS = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

COLORES = {
    'I': (0, 255, 255),  # Cyan
    'O': (255, 255, 0),  # Amarillo
    'T': (128, 0, 128),  # Morado
    'S': (0, 255, 0),    # Verde
    'Z': (255, 0, 0),    # Rojo
    'J': (0, 0, 255),    # Azul
    'L': (255, 165, 0)   # Naranja
}

def crear_tablero():
    return [[0] * ANCHO_TABLERO for _ in range(ALTO_TABLERO)]

def dibujar_tablero(tablero):
    pantalla.fill(COLOR_FONDO)
    for fila in range(ALTO_TABLERO):
        for columna in range(ANCHO_TABLERO):
            if tablero[fila][columna] != 0:
                color = tablero[fila][columna]
                pygame.draw.rect(pantalla, color,
                                 (columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
            pygame.draw.rect(pantalla, COLOR_LINEA,
                             (columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA), 1)

def dibujar_pieza_actual(tablero, pieza, color, x, y):
    sombra_y = calcular_sombra(tablero, pieza, x, y)
    for fila in range(len(pieza)):
        for columna in range(len(pieza[fila])):
            if pieza[fila][columna] != 0:

                pygame.draw.rect(pantalla, COLOR_SOMBRA,
                                 ((x + columna) * TAMANO_CELDA, (sombra_y + fila) * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(pantalla, color,
                                 ((x + columna) * TAMANO_CELDA, (y + fila) * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(pantalla, COLOR_LINEA,
                                 ((x + columna) * TAMANO_CELDA, (y + fila) * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA), 1)

def calcular_sombra(tablero, pieza, x, y):
    sombra_y = y
    while not colision(tablero, pieza, x, sombra_y):
        sombra_y += 1
    return sombra_y - 1

def nueva_pieza():
    tipo_pieza = random.choice(list(PIEZAS.keys()))
    return PIEZAS[tipo_pieza], COLORES[tipo_pieza]

def colision(tablero, pieza, x, y):
    for fila in range(len(pieza)):
        for columna in range(len(pieza[fila])):
            if pieza[fila][columna] != 0:
                if (x + columna < 0 or x + columna >= ANCHO_TABLERO or y + fila >= ALTO_TABLERO):
                    return True
                if tablero[y + fila][x + columna] != 0:
                    return True
    return False

def fijar_pieza(tablero, pieza, x, y, color):
    for fila in range(len(pieza)):
        for columna in range(len(pieza[fila])):
            if pieza[fila][columna] != 0:
                tablero[y + fila][x + columna] = color
    eliminar_filas_completas(tablero)  

def eliminar_filas_completas(tablero):
    filas_eliminadas = 0
    for fila in range(ALTO_TABLERO - 1, -1, -1):  
        if 0 not in tablero[fila]:
            del tablero[fila]  
            tablero.insert(0, [0] * ANCHO_TABLERO)  
            filas_eliminadas += 1

def rotar_pieza(pieza, tablero, x, y):
    pieza_rotada = [list(fila) for fila in zip(*pieza[::-1])]
    if not colision(tablero, pieza_rotada, x, y):
        return pieza_rotada
    return pieza  # Si hay colisión, retorna sin rotar
    
def mostrar_game_over(tiempo_total):
    texto_game_over = fuente.render("Game Over", True, (255, 0, 0))
    texto_tiempo = fuente.render(f"Tiempo: {tiempo_total:.2f} s", True, (255, 255, 255))
    pantalla.blit(texto_game_over, (ANCHO_PANTALLA // 2 - texto_game_over.get_width() // 2, ALTO_PANTALLA // 2 - 50))
    pantalla.blit(texto_tiempo, (ANCHO_PANTALLA // 2 - texto_tiempo.get_width() // 2, ALTO_PANTALLA // 2 + 10))
    pygame.display.flip()
    pygame.time.delay(3000) 



def juego():
    tablero = crear_tablero()
    pieza, color = nueva_pieza()
    x, y = ANCHO_TABLERO // 2 - len(pieza[0]) // 2, 0
    reloj = pygame.time.Clock()
    contador_bajada = 0

    tiempo_inicio = time.time()
    
    ejecutando = True
    while ejecutando:
        pantalla.fill(COLOR_FONDO)
        dibujar_tablero(tablero)
        dibujar_pieza_actual(tablero, pieza, color, x, y)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and not colision(tablero, pieza, x - 1, y):
                    x -= 1
                elif evento.key == pygame.K_RIGHT and not colision(tablero, pieza, x + 1, y):
                    x += 1
                elif evento.key == pygame.K_DOWN and not colision(tablero, pieza, x, y + 1):
                    y += 1
                elif evento.key == pygame.K_UP:
                    pieza = rotar_pieza(pieza, tablero, x, y)

        contador_bajada += 1
        if contador_bajada >= 20:
            if not colision(tablero, pieza, x, y + 1):
                y += 1
            else:
                fijar_pieza(tablero, pieza, x, y, color)
                pieza, color = nueva_pieza()
                x, y = ANCHO_TABLERO // 2 - len(pieza[0]) // 2, 0
                if colision(tablero, pieza, x, y):
                    print("Game Over")
                    ejecutando = False
            contador_bajada = 0

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

juego()
