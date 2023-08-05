import subprocess
import multiprocessing
import random
import time
from faker import Faker
import os
import matplotlib.pyplot as plt

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
    probabilities = [0.001, 0.01, 0.1]
    methods = [1,2]

    resultados = {'hamming':{"0.001":{"clean":0, "error":0, "corrected":0}, "0.01":{"clean":0, "error":0, "corrected":0}, "0.1":{"clean":0, "error":0, "corrected":0}}, 'crc32':{"0.001":{"clean":0, "error":0}, "0.01":{"clean":0, "error":0}, "0.1":{"clean":0, "error":0}}}

    iteraciones = int(input("Ingrese la cantidad de iteraciones: "))

    for metodo in methods:

        for probabilidad in probabilities:

            clean_counts_crc32 = 0
            error_counts_crc32 = 0
            corrected_counts_crc32 = 0

            clean_counts_hamming = 0
            error_counts_hamming = 0
            corrected_counts_hamming = 0

            # Datos para graficar
            labels = ['Clean', 'Error', 'Corrected']
            x = range(len(labels))

            for _ in range(iteraciones):
                receptor_process = multiprocessing.Process(target=run_receptor, args=(metodo,))
                receptor_process.start()
                time.sleep(2)

                emisor_process = multiprocessing.Process(target=run_emisor, args=(mensaje, metodo, probabilidad))
                emisor_process.start()

                emisor_process.join()
                receptor_process.join()

                time.sleep(2)
                with open("resultados.txt", "r") as file:

                    # Se lee el resultado del receptor
                    resultado = file.readline()
                   

                    if resultado == 'corrected':
                        if metodo == 1:
                            if probabilidad == 0.001:
                                resultados['hamming']['0.001']['corrected'] += 1
                            elif probabilidad == 0.01:
                                resultados['hamming']['0.01']['corrected'] += 1
                            elif probabilidad == 0.1:
                                resultados['hamming']['0.1']['corrected'] += 1

                            corrected_counts_hamming += 1

                        elif metodo == 2:
                            if probabilidad == 0.001:
                                resultados['crc32']['0.001']['corrected'] += 1
                            elif probabilidad == 0.01:
                                resultados['crc32']['0.01']['corrected'] += 1
                            elif probabilidad == 0.1:
                                resultados['crc32']['0.1']['corrected'] += 1

                            corrected_counts_crc32 += 1

                    elif resultado == 'error':
                        if metodo == 1:
                            if probabilidad == 0.001:
                                resultados['hamming']['0.001']['error'] += 1
                            elif probabilidad == 0.01:
                                resultados['hamming']['0.01']['error'] += 1
                            elif probabilidad == 0.1:
                                resultados['hamming']['0.1']['error'] += 1

                            error_counts_hamming += 1

                        elif metodo == 2:
                            if probabilidad == 0.001:
                                resultados['crc32']['0.001']['error'] += 1
                            elif probabilidad == 0.01:
                                resultados['crc32']['0.01']['error'] += 1
                            elif probabilidad == 0.1:
                                resultados['crc32']['0.1']['error'] += 1

                            error_counts_crc32 += 1

                    elif resultado == 'clean':
                        if metodo == 1:
                            if probabilidad == 0.001:
                                resultados['hamming']['0.001']['clean'] += 1
                            elif probabilidad == 0.01:
                                resultados['hamming']['0.01']['clean'] += 1
                            elif probabilidad == 0.1:
                                resultados['hamming']['0.1']['clean'] += 1

                            clean_counts_hamming += 1

                        elif metodo == 2:
                            if probabilidad == 0.001:
                                resultados['crc32']['0.001']['clean'] += 1
                            elif probabilidad == 0.01:
                                resultados['crc32']['0.01']['clean'] += 1
                            elif probabilidad == 0.1:
                                resultados['crc32']['0.1']['clean'] += 1

                            clean_counts_crc32 += 1

                    #Borrar el archivo
                    os.remove("resultados.txt")

    print(resultados)

    # Graficas CRC32
    probabilidades = ["0.001", "0.01", "0.1"]
    labels = ['Clean', 'Error']  # Labels para el eje x
    x = range(len(labels))  # Valores para el eje x

    clean_001 = resultados['crc32']['0.001']['clean']
    error_001 = resultados['crc32']['0.001']['error']

    clean_01 = resultados['crc32']['0.01']['clean']
    error_01 = resultados['crc32']['0.01']['error']

    clean_1 = resultados['crc32']['0.1']['clean']
    error_1 = resultados['crc32']['0.1']['error']

    plt.subplot(1, 3, 1)
    plt.bar(x, [clean_001, error_001])
    plt.xticks(x, labels)
    plt.title('Probabilidad 0.001')

    plt.subplot(1, 3, 2)
    plt.bar(x, [clean_01, error_01])
    plt.xticks(x, labels)
    plt.title('Probabilidad 0.01')

    plt.subplot(1, 3, 3)
    plt.bar(x, [clean_1, error_1])
    plt.xticks(x, labels)
    plt.title('Probabilidad 0.1')

    plt.suptitle('CRC32 - Mensajes:' + str(len(mensaje)))
    plt.show()

    # Guardar la grafica
    nombre = "crc32_" + str(len(mensaje)) + ".jpg"
    plt.savefig(nombre)


    # Graficas Hamming
    probabilidades = ["0.001", "0.01", "0.1"]
    labels = ['Clean', 'Error', 'Corrected']  # Labels para el eje x
    x = range(len(labels))  # Valores para el eje x

    clean_001 = resultados['hamming']['0.001']['clean']
    error_001 = resultados['hamming']['0.001']['error']
    corrected_001 = resultados['hamming']['0.001']['corrected']

    clean_01 = resultados['hamming']['0.01']['clean']
    error_01 = resultados['hamming']['0.01']['error']
    corrected_01 = resultados['hamming']['0.01']['corrected']

    clean_1 = resultados['hamming']['0.1']['clean']
    error_1 = resultados['hamming']['0.1']['error']
    corrected_1 = resultados['hamming']['0.1']['corrected']

    plt.subplot(1, 3, 1)
    plt.bar(x, [clean_001, error_001, corrected_001])
    plt.xticks(x, labels)
    plt.title('Probabilidad 0.001')

    plt.subplot(1, 3, 2)
    plt.bar(x, [clean_01, error_01, corrected_01])
    plt.xticks(x, labels)
    plt.title('Probabilidad 0.01')

    plt.subplot(1, 3, 3)
    plt.bar(x, [clean_1, error_1, corrected_1])
    plt.xticks(x, labels)
    plt.title('Probabilidad 0.1')

    plt.suptitle('Hamming - Mensajes:' + str(len(mensaje)))
    plt.show()

    # Guardar la grafica
    nombre = "hamming_" + str(len(mensaje)) + ".jpg"
    plt.savefig(nombre)



        