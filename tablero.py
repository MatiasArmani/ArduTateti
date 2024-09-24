import pygame
from Constantes import*

class Tablero:
    def __init__(self):
        self.casilleros = {}
        
    def añadir_casillero(self, nro, y, x):
        casillero = Celda(nro, x, y)
        self.casilleros[nro] = casillero

    def dibujar(self, ventana, estado_tablero):
        #ventana.fill(WHITE)
        for casillero in self.casilleros.values():
            casillero.dibujar(ventana, estado_tablero)


        # Dibujar las instrucciones en la parte superior
        fuente = pygame.font.SysFont(None, 24)
        opciones_de_usuario = [
            "Haga click encima del casillero donde desea posicionarse",
            "Presione ESC o click en cruz roja para salir"
        ]
        y_posicion = 50
        for linea in opciones_de_usuario:
            texto = fuente.render(linea, True, NEGRO)
            ventana.blit(texto, (50, y_posicion))
            y_posicion += 25
        
class Celda:
    def __init__(self, nro_celda, x, y):
        self.nro_celda = nro_celda
        self.x = x
        self.y = y
        self.color = BG

    def dibujar(self, screen, estado_tablero, color=None):
        rect = pygame.Rect(DESPLAZAMIENTO_COSTADO + self.x * TAMAÑO_CASILLERO, self.y * TAMAÑO_CASILLERO + ALTURA_OPCIONES, TAMAÑO_CASILLERO, TAMAÑO_CASILLERO)
        pygame.draw.rect(screen, color if color else self.color, rect)
        pygame.draw.rect(screen, BLANCO, rect, 1)
        font = pygame.font.SysFont(None, int(TAMAÑO_TEXTO))
        text = font.render(estado_tablero[self.nro_celda], True, BLANCO)
        screen.blit(text, (DESPLAZAMIENTO_COSTADO + self.x * TAMAÑO_CASILLERO + TAMAÑO_CASILLERO // 2 - text.get_width() // 2,
                           self.y * TAMAÑO_CASILLERO + ALTURA_OPCIONES + TAMAÑO_CASILLERO // 2 - text.get_height() // 2))
        
def construccion_tablero(tablero):

    tablero.añadir_casillero(0, 0, 0)
    tablero.añadir_casillero(1, 0, 1)
    tablero.añadir_casillero(2, 0, 2)
    tablero.añadir_casillero(3, 1, 0)
    tablero.añadir_casillero(4, 1, 1)
    tablero.añadir_casillero(5, 1, 2)
    tablero.añadir_casillero(6, 2, 0)
    tablero.añadir_casillero(7, 2, 1)
    tablero.añadir_casillero(8, 2, 2)