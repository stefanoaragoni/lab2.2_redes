import subprocess
import multiprocessing
import random
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
    # probabilidad = generar_numero()
    probabilidad = 0.0001

    iteraciones = int(input("Ingrese la cantidad de iteraciones: "))
    metodo = int(input("Ingrese el método deseado (1. Hamming, 2. CRC32): "))

    # Delete existing files
    if os.path.exists("hamming.txt"):
        os.remove("hamming.txt")
    if os.path.exists("crc32.txt"):
        os.remove("crc32.txt")

    clean_counts = []
    error_counts = []
    corrected_counts = []

    for _ in range(iteraciones):
        emisor_process = multiprocessing.Process(target=run_emisor, args=(mensaje, metodo, probabilidad))
        receptor_process = multiprocessing.Process(target=run_receptor, args=(metodo,))

        emisor_process.start()
        receptor_process.start()

        emisor_process.join()
        receptor_process.join()

    # Read and analyze the output files
    if os.path.exists("hamming.txt"):
        with open("hamming.txt", "r") as hamming_file:
            lines = hamming_file.readlines()
            clean_count = lines.count("clean\n")
            error_count = lines.count("error\n")
            corrected_count = lines.count("corrected\n")
            clean_counts.append(clean_count)
            error_counts.append(error_count)
            corrected_counts.append(corrected_count)
    
    if os.path.exists("crc32.txt"):
        with open("crc32.txt", "r") as crc32_file:
            lines = crc32_file.readlines()
            clean_count = lines.count("clean\n")
            error_count = lines.count("error\n")
            corrected_count = lines.count("corrected\n")
            clean_counts.append(clean_count)
            error_counts.append(error_count)
            corrected_counts.append(corrected_count)

    # Generate graphs
    plt.figure(figsize=(10, 6))
    plt.plot(clean_counts, label="Clean")
    plt.plot(error_counts, label="Error")
    plt.plot(corrected_counts, label="Corrected")
    plt.xlabel("Iteration")
    plt.ylabel("Message Count")
    plt.title("Message Status Counts")
    plt.legend()

    # Set y-axis limits for better visualization
    plt.ylim(bottom=0, top=max(max(clean_counts), max(error_counts), max(corrected_counts)) + 5)

    plt.show()

    


