import pygame
import random
import time
import os

ANCHO_TABLERO, ALTO_TABLERO = 10, 20 # tamaño de la matriz principal 
TAMANO_CELDA = 30 
ANCHO_PANTALLA = (ANCHO_TABLERO * TAMANO_CELDA) + 200 
ALTO_PANTALLA = ALTO_TABLERO * TAMANO_CELDA  
COLOR_FONDO = (0, 0, 0)
COLOR_LINEA = (50, 50, 50)
COLOR_SOMBRA = (200, 200, 200)
COLOR_DESTELLO = (255, 255, 255)  

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Tetris Valeria - Isabela")
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
    return [[0] * ANCHO_TABLERO for _ in range(ALTO_TABLERO)] #creacion matriz principal vacía

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

MARGEN_HORIZONTAL = (ANCHO_PANTALLA - ANCHO_TABLERO * TAMANO_CELDA) // 2

def eliminar_lineas_completas(tablero):
    lineas_borradas = 0
    filas_a_eliminar = []

    for fila in range(ALTO_TABLERO):
        if 0 not in tablero[fila]:
            filas_a_eliminar.append(fila)

    for fila in filas_a_eliminar:
        for columna in range(ANCHO_TABLERO):
            pygame.draw.rect(
                pantalla,
                COLOR_DESTELLO,  
                ((columna + MARGEN_HORIZONTAL) * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA)
            )

        pygame.display.update()  
        pygame.time.delay(200)  

    for fila in filas_a_eliminar:
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

def dibujar_pieza_siguiente(pieza, color): #dibuja la pieza sigueinte
    offset_x, offset_y = ANCHO_TABLERO + 1, 3  
    for fila in range(len(pieza)):
        for columna in range(len(pieza[fila])):
            if pieza[fila][columna] != 0:
                pygame.draw.rect(pantalla, color,
                                 ((offset_x + columna) * TAMANO_CELDA, (offset_y + fila) * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(pantalla, COLOR_LINEA,
                                 ((offset_x + columna) * TAMANO_CELDA, (offset_y + fila) * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA), 1)

def pantalla_final(puntaje, tiempo_total):
    ejecutando = True
    while ejecutando:
        pantalla.fill((0, 0, 0))  

        mensaje_texto = fuente.render("¡Juego Terminado!", True, (255, 255, 255))
        pantalla.blit(mensaje_texto, (ANCHO_PANTALLA // 2 - mensaje_texto.get_width() // 2, ALTO_PANTALLA // 2 - 100))

        puntaje_texto = fuente.render(f"Puntaje final: {puntaje}", True, (255, 255, 255))
        pantalla.blit(puntaje_texto, (ANCHO_PANTALLA // 2 - puntaje_texto.get_width() // 2, ALTO_PANTALLA // 2 - 50))

        tiempo_texto = fuente.render(f"Tiempo total: {tiempo_total}s", True, (255, 255, 255))
        pantalla.blit(tiempo_texto, (ANCHO_PANTALLA // 2 - tiempo_texto.get_width() // 2, ALTO_PANTALLA // 2))

        opcion_reintentar = fuente.render("Presiona R para volver a jugar", True, (255, 255, 255))
        pantalla.blit(opcion_reintentar, (ANCHO_PANTALLA // 2 - opcion_reintentar.get_width() // 2, ALTO_PANTALLA // 2 + 50))

        opcion_salir = fuente.render("Presiona Q para salir", True, (255, 255, 255))
        pantalla.blit(opcion_salir, (ANCHO_PANTALLA // 2 - opcion_salir.get_width() // 2, ALTO_PANTALLA // 2 + 100))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r: 
                    return True
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    exit()
def juego():
    global pantalla #Variable de instancia 
    pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    info_pantalla = pygame.display.Info()
    global ANCHO_PANTALLA, ALTO_PANTALLA, TAMANO_CELDA, ANCHO_TABLERO, ALTO_TABLERO

    ANCHO_PANTALLA = info_pantalla.current_w
    ALTO_PANTALLA = info_pantalla.current_h
    TAMANO_CELDA = min(ALTO_PANTALLA // ALTO_TABLERO, (ANCHO_PANTALLA - 400) // ANCHO_TABLERO)

    offset_x = (ANCHO_PANTALLA - (ANCHO_TABLERO * TAMANO_CELDA)) // 2
    offset_y = (ALTO_PANTALLA - (ALTO_TABLERO * TAMANO_CELDA)) // 2

    while True:
        tablero = crear_tablero()
        pieza, color = nueva_pieza()
        siguiente_pieza, siguiente_color = nueva_pieza()
        x, y = ANCHO_TABLERO // 2 - len(pieza[0]) // 2, 0
        reloj = pygame.time.Clock()
        contador_bajada = 0
        puntaje = 0
        tiempo_inicio = time.time()
        ejecutando = True

        while ejecutando:
            pantalla.fill((50, 50, 50))  

            pygame.draw.rect(pantalla, COLOR_FONDO,
                             (offset_x, offset_y, ANCHO_TABLERO * TAMANO_CELDA, ALTO_TABLERO * TAMANO_CELDA))

            dibujar_tablero_centrado(tablero, offset_x, offset_y)
            dibujar_pieza_actual_centrada(tablero, pieza, color, x, y, offset_x, offset_y)
            
            pygame.draw.rect(pantalla, (50, 50, 50), (offset_x + ANCHO_TABLERO * TAMANO_CELDA, offset_y,
                                                      ANCHO_PANTALLA - (offset_x + ANCHO_TABLERO * TAMANO_CELDA),
                                                      ALTO_TABLERO * TAMANO_CELDA))

            dibujar_pieza_siguiente_centrada(siguiente_pieza, siguiente_color, offset_x + ANCHO_TABLERO * TAMANO_CELDA)
            puntaje_texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
            pantalla.blit(puntaje_texto, (offset_x + ANCHO_TABLERO * TAMANO_CELDA + 10, offset_y + 10))
            
            tiempo_transcurrido = int(time.time() - tiempo_inicio)
            tiempo_texto = fuente.render(f"Tiempo: {tiempo_transcurrido}s", True, (255, 255, 255))
            pantalla.blit(tiempo_texto, (offset_x + ANCHO_TABLERO * TAMANO_CELDA + 10, offset_y + 50))

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif evento.key == pygame.K_LEFT:
                        if not colision(tablero, pieza, x - 1, y):
                            x -= 1
                    elif evento.key == pygame.K_RIGHT:
                        if not colision(tablero, pieza, x + 1, y):
                            x += 1
                    elif evento.key == pygame.K_DOWN:
                        if not colision(tablero, pieza, x, y + 1):
                            y += 1
                    elif evento.key == pygame.K_UP:
                        pieza, x = rotar_pieza(pieza, tablero, x, y)

            if contador_bajada == 30:
                if not colision(tablero, pieza, x, y + 1):
                    y += 1
                else:
                    lineas_borradas = fijar_pieza(tablero, pieza, x, y, color)
                    puntaje = actualizar_puntaje(lineas_borradas, puntaje)
                    pieza, color = siguiente_pieza, siguiente_color
                    siguiente_pieza, siguiente_color = nueva_pieza()
                    x, y = ANCHO_TABLERO // 2 - len(pieza[0]) // 2, 0
                    if colision(tablero, pieza, x, y):
                        ejecutando = False
                contador_bajada = 0

            pygame.display.flip()
            reloj.tick(60)
            contador_bajada += 1

        tiempo_total = int(time.time() - tiempo_inicio)
        if not pantalla_final(puntaje, tiempo_total):
            break

def dibujar_tablero_centrado(tablero, offset_x, offset_y):
    for fila in range(ALTO_TABLERO):
        for columna in range(ANCHO_TABLERO):
            if tablero[fila][columna] != 0:
                color = tablero[fila][columna]
                pygame.draw.rect(pantalla, color,
                                 (offset_x + columna * TAMANO_CELDA, offset_y + fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
            pygame.draw.rect(pantalla, COLOR_LINEA,
                             (offset_x + columna * TAMANO_CELDA, offset_y + fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA), 1)


def dibujar_pieza_actual_centrada(tablero, pieza, color, x, y, offset_x, offset_y):
    sombra_y = calcular_sombra(tablero, pieza, x, y)
    for fila in range(len(pieza)):
        for columna in range(len(pieza[fila])):
            if pieza[fila][columna] != 0:
                pygame.draw.rect(pantalla, COLOR_SOMBRA,
                                 (offset_x + (x + columna) * TAMANO_CELDA,
                                  offset_y + (sombra_y + fila) * TAMANO_CELDA,
                                  TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(pantalla, color,
                                 (offset_x + (x + columna) * TAMANO_CELDA,
                                  offset_y + (y + fila) * TAMANO_CELDA,
                                  TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(pantalla, COLOR_LINEA,
                                 (offset_x + (x + columna) * TAMANO_CELDA,
                                  offset_y + (y + fila) * TAMANO_CELDA,
                                  TAMANO_CELDA, TAMANO_CELDA), 1)


def dibujar_pieza_siguiente_centrada(pieza, color, offset_x):
    offset_y = (ALTO_PANTALLA - len(pieza) * TAMANO_CELDA) // 2
    for fila in range(len(pieza)):
        for columna in range(len(pieza[fila])):
            if pieza[fila][columna] != 0:
                pygame.draw.rect(pantalla, color,
                                 (offset_x + columna * TAMANO_CELDA,
                                  offset_y + fila * TAMANO_CELDA,
                                  TAMANO_CELDA, TAMANO_CELDA))
                pygame.draw.rect(pantalla, COLOR_LINEA,
                                 (offset_x + columna * TAMANO_CELDA,
                                  offset_y + fila * TAMANO_CELDA,
                                  TAMANO_CELDA, TAMANO_CELDA), 1)


if __name__ == "__main__":
    juego()
