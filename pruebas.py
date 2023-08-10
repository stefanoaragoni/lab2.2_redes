import subprocess
import multiprocessing
import random
from faker import Faker
import os
import matplotlib.pyplot as plt
import time

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
    mensajes = ["Hola como estas", "Habia una vez un lind gatito negro llamdo chimuelo"]
    probabilities = [0.001, 0.01, 0.1]
    methods = [1,2]

    iteraciones = int(input("Ingrese la cantidad de iteraciones: "))

    for metodo in methods:

        for probabilidad in probabilities:

            for mensaje in mensajes:

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

                    receptor_process.join()
                    emisor_process.join()
                    time.sleep(1)
                    

                # Read and analyze the output files
                if os.path.exists("hamming.txt"):
                    with open("hamming.txt", "r") as hamming_file:
                        lines = hamming_file.readlines()
                        clean_count = lines.count("clean\n")
                        error_count = lines.count("error\n")
                        corrected_count = lines.count("corrected\n")
                        clean_counts_hamming =+ clean_count
                        error_counts_hamming =+ error_count
                        corrected_counts_hamming =+ corrected_count

                    hamming_counts = [clean_counts_hamming, error_counts_hamming, corrected_counts_hamming]

                    with open("hamming.txt", "w") as hamming_file:
                        hamming_file.truncate(0)

                if os.path.exists("crc32.txt"):
                    with open("crc32.txt", "r") as crc32_file:
                        lines = crc32_file.readlines()
                        clean_count = lines.count("clean\n")
                        error_count = lines.count("error\n")
                        corrected_count = lines.count("corrected\n")
                        clean_counts_crc32 =+ clean_count
                        error_counts_crc32 =+ error_count
                        corrected_counts_crc32 =+ corrected_count

                    crc32_counts = [clean_counts_crc32, error_counts_crc32, corrected_counts_crc32]

                    with open("crc32.txt", "w") as crc32_file:
                        crc32_file.truncate(0)

                
                if metodo == 1:
                    # Gráfica de Hamming
                    hamming_counts = [clean_counts_hamming, error_counts_hamming, corrected_counts_hamming]
                    plt.bar(x, hamming_counts, align='center')
                    plt.xlabel('Result Type')
                    plt.ylabel('Count')
                    plt.title('Hamming con probabilidad de ' + str(probabilidad) + ' y largo de cadena '  +str(len(mensaje)))
                    plt.xticks(x, labels)
                    plt.savefig('hamming_' + str(probabilidad) + "_"  +str(len(mensaje)) +'.png')
                    plt.clf()

                else:

                    # Gráfica de CRC32
                    crc32_counts = [clean_counts_crc32, error_counts_crc32, corrected_counts_crc32]
                    plt.bar(x, crc32_counts, align='center')
                    plt.xlabel('Result Type')
                    plt.ylabel('Count')
                    plt.title('CRC32 con probabilida de ' + str(probabilidad) +  ' y largo de cadena '  +str(len(mensaje)))
                    plt.xticks(x, labels)
                    plt.savefig('crc32_' + str(probabilidad) + "_"  +str(len(mensaje)) +'.png')
                    plt.clf()
