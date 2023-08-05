import subprocess
import multiprocessing
import random
from faker import Faker

def run_emisor(mensaje, metodo, probabilidad):
    subprocess.run(["python", "emisor.py", mensaje, str(metodo), str(probabilidad)])

def run_receptor(metodo):
    subprocess.run(["javac", "receptor.java"])
    subprocess.run(["java", "receptor", str(metodo)])

def generar_numero():
    return random.random() * (1.0 - 1e-10)

def generar_mensaje():
    fake = Faker()
    mensaje = fake.paragraph(nb_sentences=random.randint(1, 10))

    return mensaje


if __name__ == "__main__":
    mensaje = generar_mensaje()
    # probabilidad = generar_numero()
    probabilidad = 1

    iteraciones = int(input("Ingrese la cantidad de iteraciones: "))
    metodo = int(input("Ingrese el método deseado (1. Hamming, 2. CRC32): "))

    for _ in range(iteraciones):
        emisor_process = multiprocessing.Process(target=run_emisor, args=(mensaje, metodo, probabilidad))
        receptor_process = multiprocessing.Process(target=run_receptor, args=(metodo,))

        emisor_process.start()
        receptor_process.start()

        emisor_process.join()
        receptor_process.join()


