import random
import math
import os
import pygame
from humano import Humano
from Constantes import*
from tablero import Tablero,Celda,construccion_tablero
from COM import ConexionSerie
import time

class TaTeTi:
    def __init__(self):
        self.tablero = ['-' for _ in range(9)]

        puerto = input("Introduce el puerto del dispositivo serie: ")
        baudrate_input = input("Introduce el baudrate: ")
        self.conexion_serie = ConexionSerie(puerto, baudrate_input) if puerto and baudrate_input else None
        self.conexion_serie.abrir_conexion()

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
                self.conexion_serie.enviar_comando(":H"+str(cuadrado+1))
                pygame.display.flip()
                if self.verificar_ganador():
                    self.conexion_serie.enviar_comando("reiniciar")
                    self.conexion_serie.cerrar_conexion()
                    break
                
                #Bot
                print("Computadora pensando..")
                pygame.time.delay(DELAY)  # Retardo de 300ms para visualizar el progreso

                time.sleep(1)
                
                cuadrado = bot.movimiento_bot(self.tablero)
                self.tablero[cuadrado] = self.agente
                tablero_grafico.dibujar(ventana, self.tablero)
                self.conexion_serie.enviar_comando(":B"+str(cuadrado+1))
                if self.verificar_ganador():
                    self.conexion_serie.enviar_comando("reiniciar")
                    self.conexion_serie.cerrar_conexion()
                    break

                posicion = 0
            pygame.display.flip()
            reloj.tick(FPS)

        # showing the final view of tablero
        print()
        self.mostrar_tablero()
        
        pygame.quit()
        

        
class Bot(TaTeTi):
    def __init__(self,letra):
        self.agente = letra
        self.humano = "X" if letra == "O" else "O"

    def jugadores(self,estado_tablero):
        n = len(estado_tablero)
        x = 0
        o = 0
        for i in range(9):
            if(estado_tablero[i] == "X"):
                x = x+1
            if(estado_tablero[i] == "O"):
                o = o+1
        
        if(self.humano == "X"):
            return "X" if x==o else "O"
        if(self.humano == "O"):
            return "O" if x==o else "X"
    
    def movimientos_disponibles(self,estado_tablero):
        return [i for i, x in enumerate(estado_tablero) if x == "-"]
    
    def tablero_modificado(self,estado_tablero,movimiento):
        nuevo_estado = estado_tablero.copy()
        jugador = self.jugadores(estado_tablero)
        nuevo_estado[movimiento] = jugador
        return nuevo_estado
    
    def terminal(self,estado_tablero):
        if(self.victoria_jugador(estado_tablero,"X")):
            return True
        if(self.victoria_jugador(estado_tablero,"O")):
            return True
        return False

    def heuristica(self, estado_tablero, jugador):
        humano = self.humano  # yourself
        otro_jugador = 'O' if jugador == 'X' else 'X'

        # first we want to check if the previous move is a winner
        if self.terminal(estado_tablero):
            return {'posicion': None, 'valoracion_jugada': 1 * (len(self.movimientos_disponibles(estado_tablero)) + 1) if otro_jugador == humano else -1 * (
                        len(self.movimientos_disponibles(estado_tablero)) + 1)}
        elif self.tablero_completado(estado_tablero):
            return {'posicion': None, 'valoracion_jugada': 0}

        if jugador == humano:
            mejor_jugada = {'posicion': None, 'valoracion_jugada': -math.inf}  # each valoracion_jugada should maximize
        else:
            mejor_jugada = {'posicion': None, 'valoracion_jugada': math.inf}  # each valoracion_jugada should minimize
        for movimiento_posible in self.movimientos_disponibles(estado_tablero):
            nuevo_estado = self.tablero_modificado(estado_tablero,movimiento_posible)
            sim_score = self.heuristica(nuevo_estado, otro_jugador)  # simulate a game after making that move

            sim_score['posicion'] = movimiento_posible  # this represents the move optimal next move

            if jugador == humano:  # X is max jugador
                if sim_score['valoracion_jugada'] > mejor_jugada['valoracion_jugada']:
                    mejor_jugada = sim_score
            else:
                if sim_score['valoracion_jugada'] < mejor_jugada['valoracion_jugada']:
                    mejor_jugada = sim_score
        return mejor_jugada

    def movimiento_bot(self,estado_tablero):
        cuadrado = self.heuristica(estado_tablero,self.agente)['posicion']
        return cuadrado