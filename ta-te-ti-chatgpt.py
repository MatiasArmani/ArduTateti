# Configuración de colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
GRIS = (200, 200, 200)
BG = (0, 0, 20)
AMARILLO = (255, 255, 0)

# Dimensiones
ANCHO = 600
ALTO = 500  
TAMAÑO_CASILLERO = 80
TAMAÑO_TEXTO = TAMAÑO_CASILLERO * 0.8
ALTURA_OPCIONES = 100
DESPLAZAMIENTO_COSTADO = 150

#Otros parametros
COSTO_UNITARIO = 1
COSTO_EXTRA = 30
POSICION_TEXTO = (10,10)
DELAY = 300

# FPS
FPS = 60

import random
import math
import os
import pygame

class Humano:
    def __init__(self,letter):
        self.letter = letter
    
    def jugada_humano(self,estado_tablero,posicion):
        # taking user input
        while True:
            #cuadrado =  int(input("Ingrese el cuadrado donde desea posicionarse (1-9): "))
            cuadrado = posicion
            print()
            if estado_tablero[cuadrado-1] == "-":
                break
        return cuadrado-1

class TaTeTi:
    def __init__(self):
        self.tablero = ['-' for _ in range(9)]
        if random.randint(0, 1) == 1:
            self.humano = 'X'
            self.agente = "O"
        else:
            self.humano = "O"
            self.agente = "X"

    def mostrar_tablero(self):
        print("")
        for i in range(3):
            print("  ",self.tablero[0+(i*3)]," | ",self.tablero[1+(i*3)]," | ",self.tablero[2+(i*3)])
            print("")
            
    def tablero_completado(self,estado_tablero):
        return not "-" in estado_tablero

    def victoria_jugador(self,estado_tablero,jugador):
        if estado_tablero[0]==estado_tablero[1]==estado_tablero[2] == jugador: return True
        if estado_tablero[3]==estado_tablero[4]==estado_tablero[5] == jugador: return True
        if estado_tablero[6]==estado_tablero[7]==estado_tablero[8] == jugador: return True
        if estado_tablero[0]==estado_tablero[3]==estado_tablero[6] == jugador: return True
        if estado_tablero[1]==estado_tablero[4]==estado_tablero[7] == jugador: return True
        if estado_tablero[2]==estado_tablero[5]==estado_tablero[8] == jugador: return True
        if estado_tablero[0]==estado_tablero[4]==estado_tablero[8] == jugador: return True
        if estado_tablero[2]==estado_tablero[4]==estado_tablero[6] == jugador: return True

        return False

    def verificar_ganador(self):
        if self.victoria_jugador(self.tablero,self.humano):
            os.system("cls")
            print("Has ganado la partida! ")
            return True
            
        if self.victoria_jugador(self.tablero,self.agente):
            os.system("cls")
            print("El bot ha ganado la partida! ")
            return True

        # checking whether the game is draw or not
        if self.tablero_completado(self.tablero):
            os.system("cls")
            print("Partido Empatado!")
            return True
        return False

    def inicio(self):
        
        # Inicializar Pygame
        pygame.init()
        ventana = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Ta-Te-Ti")
        reloj = pygame.time.Clock()
        
        
        bot = Bot(self.agente)
        humano = Humano(self.humano)
        
        tablero_grafico = Tablero()
        construccion_tablero(tablero_grafico)
        
        running = True
        posicion = 0
        
        estado = "en ejecucion"
        
        while running:
            # os.system("cls")
            # print("Es tu turno!")
            # self.mostrar_tablero()
            
            ventana.fill(pygame.Color('CadetBlue1'))
            tablero_grafico.dibujar(ventana, self.tablero)
            
            # Registramos eventos de teclado y ratón.
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Cerrar programa desde la cruz de ventana
                    running = False
                    pygame.quit()
                    return "fin"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # Cerrar programa con la tecla ESCAPE
                        running = False
                        pygame.quit()
                        return "fin"
                    if event.key == pygame.K_1:
                        posicion = 1
                    elif event.key == pygame.K_2:
                        posicion = 2
                    if event.key == pygame.K_3:
                        posicion = 3
                    elif event.key == pygame.K_4:
                        posicion = 4
                    if event.key == pygame.K_5:
                        posicion = 5
                    elif event.key == pygame.K_6:
                        posicion = 6
                    if event.key == pygame.K_7:
                        posicion = 7
                    elif event.key == pygame.K_8:
                        posicion = 8
                    if event.key == pygame.K_9:
                        posicion = 9

            if posicion!=0:
                #Human
                cuadrado = humano.jugada_humano(self.tablero, posicion)
                self.tablero[cuadrado] = self.humano
                tablero_grafico.dibujar(ventana, self.tablero)
                pygame.display.flip()
                if self.verificar_ganador():
                    break
                
                #Bot
                print("Computadora pensando..")
                pygame.time.delay(DELAY)  # Retardo de 300ms para visualizar el progreso
                
                cuadrado = bot.movimiento_bot(self.tablero)
                self.tablero[cuadrado] = self.agente
                tablero_grafico.dibujar(ventana, self.tablero)
                if self.verificar_ganador():
                    break

                posicion = 0
            pygame.display.flip()
            reloj.tick(FPS)

        # showing the final view of tablero
        print()
        self.mostrar_tablero()
        
        pygame.quit()
        

        
class Bot(TaTeTi):
    def __init__(self, letra):
        self.agente = letra
        self.humano = "X" if letra == "O" else "O"

    def movimientos_disponibles(self, estado_tablero):
        return [i for i, x in enumerate(estado_tablero) if x == "-"]

    def tablero_modificado(self, estado_tablero, movimiento, jugador):
        nuevo_estado = estado_tablero.copy()
        nuevo_estado[movimiento] = jugador
        return nuevo_estado

    def victoria_jugador(self, estado_tablero, jugador):
        # Verificar todas las posibles combinaciones ganadoras
        combinaciones_ganadoras = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combinacion in combinaciones_ganadoras:
            if estado_tablero[combinacion[0]] == estado_tablero[combinacion[1]] == estado_tablero[combinacion[2]] == jugador:
                return True
        return False

    def heuristica(self, estado_tablero, jugador):
        if self.victoria_jugador(estado_tablero, self.agente):
            return 10  # La mejor situación posible para el bot
        elif self.victoria_jugador(estado_tablero, self.humano):
            return -10  # La peor situación posible para el bot
        else:
            return 0  # Ni ganador ni perdedor (posible empate o juego aún en curso)

    def recocido_simulado(self, estado_tablero, temperatura_inicial=100, tasa_enfriamiento=0.99, temperatura_minima=1):
        temperatura = temperatura_inicial
        mejor_movimiento = None
        mejor_valoracion = -math.inf

        while temperatura > temperatura_minima:
            # Elegir un movimiento aleatorio entre los disponibles
            posibles_movimientos = self.movimientos_disponibles(estado_tablero)
            movimiento_actual = random.choice(posibles_movimientos)
            estado_modificado = self.tablero_modificado(estado_tablero, movimiento_actual, self.agente)

            # Evaluar la heurística del nuevo estado
            valoracion_actual = self.heuristica(estado_modificado, self.agente)

            # Comparar la heurística con la mejor encontrada hasta ahora
            if valoracion_actual > mejor_valoracion:
                mejor_valoracion = valoracion_actual
                mejor_movimiento = movimiento_actual

            # Calcular la probabilidad de aceptar un movimiento peor
            probabilidad_aceptacion = math.exp((valoracion_actual - mejor_valoracion) / temperatura)
            if random.uniform(0, 1) < probabilidad_aceptacion:
                mejor_valoracion = valoracion_actual
                mejor_movimiento = movimiento_actual

            # Reducir la temperatura
            temperatura *= tasa_enfriamiento

        return mejor_movimiento

    def movimiento_bot(self, estado_tablero):
        cuadrado = self.recocido_simulado(estado_tablero)
        return cuadrado

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

def main():
    
    estado = "en ejecucion"
    
    while True:
        # starting the game
        ta_te_ti = TaTeTi()
        estado = ta_te_ti.inicio()
        if estado == "fin":
            break

if __name__ == "__main__":
    main()