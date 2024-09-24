import serial

class ConexionSerie:
    def __init__(self, puerto, baudrate, timeout=2):
        self.puerto = puerto
        self.baudrate = self.__validar_baudrate(baudrate)
        self.timeout = timeout # En segundos. Tiempo máximo de espera para leer datos
        self.conexion = None

    def __validar_baudrate(self, baudrate):
        try:
            baudrate_int = int(baudrate)
            if baudrate_int <= 0:
                raise ValueError("El baudrate debe ser un número entero positivo.")
            return baudrate_int
        except ValueError as e:
            print(f"Error al configurar el baudrate: {e}")
            return 0

    def abrir_conexion(self):
        try:
            self.conexion = serial.Serial(self.puerto, self.baudrate, timeout=self.timeout)
            print(f"Conexión establecida en {self.puerto} con baudrate {self.baudrate}")
        except serial.SerialException as e:
            print(f"Error al abrir la conexión: {e}")
            exit(1)

    def leer_datos(self):
        try:
            if self.conexion and self.conexion.is_open:
                datos = []
                lineas = self.conexion.readlines()
                #print(f"Datos leídos: {lineas}")
                for linea in lineas:
                    # Decodificamos la línea de bytes a string
                    linea_str = linea.decode('utf-8').strip()

                    linea_str = linea_str.replace('"', "'")
                    datos.append(linea_str)
                
                if datos:  # Si se recibe algo
                    return datos
                else:  # Si se excede el timeout y no hay datos
                    print("Timeout alcanzado: no se recibieron datos.")
                    return None
            else:
                print("La conexión no está abierta.")
        except serial.SerialException as e:
            print(f"Error al leer datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

    def enviar_comando(self, comando):
        try:
            if self.conexion and self.conexion.is_open:
                comando += '\n'
                self.conexion.write(comando.encode())  # Enviar el carácter ingresado al Arduino
                self.conexion.flush()  # Asegurarse de que el comando se envía de inmediato
                print(f"Comando '{comando.strip()}' enviado.")
            else:
                print("La conexión no está abierta.")
        except serial.SerialException as e:
            print(f"Error al enviar comando: {e}")

    def cerrar_conexion(self):
        if self.conexion and self.conexion.is_open:
            self.conexion.close()
            print(f"Conexión en {self.puerto} cerrada.")
        else:
            print("No hay conexión abierta para cerrar.")