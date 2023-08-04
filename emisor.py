import random
import socket
from crc32_emisor import crc32
from Hamming_Emisor import calcRedundantBits, posRedundantBits, calcParityBits

class CapaTransmision:
    def __init__(self):
        self.host = 'localhost'
        self.port = 8080
        self.conectar()

    def conectar(self):
        # Se crea el socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))

    def enviar(self, mensaje):
        print("\n--> Enviando mensaje (con ruido): " + mensaje + ".")
        self.s.sendall(mensaje.encode())
        print("\n--> Mensaje enviado.\n")

    def cerrar(self):
        self.s.close()

class capaRuido:
    def __init__(self, probabilidad = 0.1):
        self.probabilidad = probabilidad

    def aplicar(self, mensaje):
        new_mensaje = ""
        print("\n--> Trama en binario (sin ruido, modificada): ", mensaje)

        for bit in mensaje:
            if random.random() < self.probabilidad:
                if bit == '0':
                    new_mensaje += '1'
                else:
                    new_mensaje += '0'

            else:
                new_mensaje += bit

        return new_mensaje
    
class capaEnlace:
    def __init__(self, metodo):
        self.metodo = metodo

    def aplicar(self, mensaje):
        
        if self.metodo == 1:
            m = len(mensaje)
            r = calcRedundantBits(m)

            arr = posRedundantBits(mensaje, r)
            arr = calcParityBits(arr, r)

            self.message = ''.join(arr)
        
        elif self.metodo == 2:
            self.message = crc32(mensaje)
        
        return self.message
    
class capaPresentacion:
    def __init__(self):
        pass

    def binario(self, mensaje):
        # Convertir texto a binario por ASCII de cada caracter.
        self.trama = "".join([bin(ord(c))[2:].zfill(8) for c in mensaje])
        print("\n--> Trama en binario (sin ruido, sin modificar): ", self.trama)

        return self.trama           

class capaAplicacion:
    def __init__(self):
        pass

    def solicitar(self):
        print("\n---------- EMISOR ----------\n")
        self.trama = input("Ingrese un mensaje: ")

        self.metodo = 0
        while True:
            print("\nSeleccione un método de codificación:")
            print("1. Hamming")
            print("2. CRC-32")

            self.metodo  = input("Ingrese el número del método: ")

            if self.metodo == "1" or self.metodo  == "2":
                self.metodo = int(self.metodo )
                break
            else:
                print("\nIngrese un valor válido\n")

        self.probabilidad = 0
        while True:
            print('\nProbabilidad de ruido')
            self.probabilidad = input("Ingrese un número entre 0 y 1: ")

            try:
                self.probabilidad = float(self.probabilidad)
                if self.probabilidad >= 0 and self.probabilidad <= 1:
                    break
                else:
                    print("\nIngrese un valor válido\n")
            except:
                print("\nIngrese un valor válido\n")

        return self.trama, self.metodo, self.probabilidad


def main():
    capa_aplicacion = capaAplicacion()
    mensaje, metodo, probabilidad = capa_aplicacion.solicitar()

    capa_presentacion = capaPresentacion()
    trama = capa_presentacion.binario(mensaje)

    capa_enlace = capaEnlace(metodo)
    binario = capa_enlace.aplicar(trama)

    capa_ruido = capaRuido(probabilidad)
    binario_ruido = capa_ruido.aplicar(binario)

    capa = CapaTransmision()
    capa.enviar(binario_ruido)
    capa.cerrar()

if __name__ == "__main__":
    main()

