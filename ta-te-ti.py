import random
import math
import os
from TaTeTiClass import TaTeTi
from humano import Humano

#X is max = 1
#O in min = -1



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