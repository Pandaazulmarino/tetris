import pygame
import random
import time

ANCHO_TABLERO, ALTO_TABLERO = 10, 20
TAMANO_CELDA = 30
ANCHO_PANTALLA = ANCHO_TABLERO * TAMANO_CELDA + 200  # Ampliado el ancho para la zona derecha
ALTO_PANTALLA = ALTO_TABLERO * TAMANO_CELDA
COLOR_FONDO = (0, 0, 0)
COLOR_LINEA = (50, 50, 50)
COLOR_SOMBRA = (200, 200, 200)
COLOR_DESTELLO = (255, 255, 255)  

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Tetris")
fuente = pygame.font.SysFont(None, 36)

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
    'I': (0, 255, 255),
    'O': (255, 255, 0),
    'T': (128, 0, 128),
    'S': (0, 255, 0),
    'Z': (255, 0, 0),
    'J': (0, 0, 255),
    'L': (255, 165, 0)
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
    lineas_borradas = eliminar_lineas_completas(tablero)  
    return lineas_borradas

def eliminar_lineas_completas(tablero):
    lineas_borradas = 0
    for fila in range(ALTO_TABLERO):
        if 0 not in tablero[fila]:
            for columna in range(ANCHO_TABLERO):
                tablero[fila][columna] = COLOR_DESTELLO
            dibujar_tablero(tablero)
            pygame.display.flip()
            pygame.time.delay(100) 

            del tablero[fila]
            tablero.insert(0, [0] * ANCHO_TABLERO)
            lineas_borradas += 1
    return lineas_borradas

def actualizar_puntaje(lineas_borradas, puntaje):
    if lineas_borradas == 1:
        puntaje += 100
    elif lineas_borradas == 2:
        puntaje += 300
    elif lineas_borradas == 3:
        puntaje += 500
    elif lineas_borradas == 4:
        puntaje += 800
    return puntaje

def rotar_pieza(pieza, tablero, x, y):
    pieza_rotada = [list(fila) for fila in zip(*pieza[::-1])]
    if not colision(tablero, pieza_rotada, x, y):
        return pieza_rotada, x
    if x > 0 and not colision(tablero, pieza_rotada, x - 1, y):
        return pieza_rotada, x - 1
    if x < ANCHO_TABLERO - len(pieza_rotada[0]) and not colision(tablero, pieza_rotada, x + 1, y):
        return pieza_rotada, x + 1
    return pieza, x

def dibujar_pieza_siguiente(pieza, color):
    """Dibuja la pieza siguiente en la parte derecha de la pantalla dentro del área extendida"""
    offset_x, offset_y = ANCHO_TABLERO + 2, 3  # Ajusta esta posición a donde desees mostrarla
    for fila in range(len(pieza)):
        for columna in range(len(pieza[fila])):
            if pieza[fila][columna] != 0:
                pygame.draw.rect(pantalla, color,
                                 ((offset_x + columna) * TAMANO_CELDA, (offset_y + fila) * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(pantalla, COLOR_LINEA,
                                 ((offset_x + columna) * TAMANO_CELDA, (offset_y + fila) * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA), 1)

def juego():
    tablero = crear_tablero()
    pieza, color = nueva_pieza()
    siguiente_pieza, siguiente_color = nueva_pieza()  # Guardamos la siguiente pieza
    x, y = ANCHO_TABLERO // 2 - len(pieza[0]) // 2, 0
    reloj = pygame.time.Clock()
    contador_bajada = 0
    puntaje = 0
    tiempo_inicio = time.time()
    ejecutando = True

    while ejecutando:
        pantalla.fill(COLOR_FONDO)
        dibujar_tablero(tablero)  # Dibuja la zona del tablero como antes
        dibujar_pieza_actual(tablero, pieza, color, x, y)

        # Agregar un fondo extendido al lado derecho del tablero
        pygame.draw.rect(pantalla, (50, 50, 50), (ANCHO_TABLERO * TAMANO_CELDA, 0, ANCHO_PANTALLA - ANCHO_TABLERO * TAMANO_CELDA, ALTO_PANTALLA)) 

        # Mostrar la siguiente pieza en ese fondo extendido
        dibujar_pieza_siguiente(siguiente_pieza, siguiente_color)

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
                    pieza, x = rotar_pieza(pieza, tablero, x, y)

        contador_bajada += 1
        if contador_bajada >= 10:
            if not colision(tablero, pieza, x, y + 1):
                y += 1
            else:
                # Fijar la pieza y obtener las líneas borradas
                lineas_borradas = fijar_pieza(tablero, pieza, x, y, color)
                puntaje = actualizar_puntaje(lineas_borradas, puntaje)
                pieza, color = siguiente_pieza, siguiente_color  # La siguiente pieza pasa a ser la actual
                siguiente_pieza, siguiente_color = nueva_pieza()  # Generar una nueva pieza siguiente
                x, y = ANCHO_TABLERO // 2 - len(pieza[0]) // 2, 0
                if colision(tablero, pieza, x, y):
                    print("Game Over")
                    tiempo_total = round(time.time() - tiempo_inicio, 2)
                    ejecutando = False
                    mostrar_game_over(tiempo_total, puntaje)
            contador_bajada = 0

        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        pantalla.blit(texto_puntaje, (10, 10))
        tiempo_actual = round(time.time() - tiempo_inicio, 2)
        texto_tiempo = fuente.render(f"Tiempo: {tiempo_actual}s", True, (255, 255, 255))
        pantalla.blit(texto_tiempo, (10, 40))

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

def mostrar_game_over(tiempo, puntaje):
    """Mostrar mensaje de game over con puntaje y tiempo"""
    pantalla.fill(COLOR_FONDO)
    mensaje = fuente.render(f"Game Over - Puntaje: {puntaje}", True, (255, 255, 255))
    tiempo_mensaje = fuente.render(f"Tiempo: {tiempo}s", True, (255, 255, 255))
    pantalla.blit(mensaje, (ANCHO_PANTALLA // 4, ALTO_PANTALLERO // 2))
    pantalla.blit(tiempo_mensaje, (ANCHO_PANTALLA // 4, ALTO_PANTALLERO // 2 + 40))
    pygame.display.flip()
    pygame.time.delay(2000)

if __name__ == "__main__":
    juego()
