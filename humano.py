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