# ░▒█▀▀▄░▒█▀▀▄░▒█▀▀▄░█▀▀█░█▀█░░░░░░░░▒█▀▀▀░▒█▀▄▀█░▀█▀░▒█▀▀▀█░▒█▀▀▀█░▒█▀▀▄
# ░▒█░░░░▒█▄▄▀░▒█░░░░░▒▀▄░▒▄▀░░░▀▀░░░▒█▀▀▀░▒█▒█▒█░▒█░░░▀▀▀▄▄░▒█░░▒█░▒█▄▄▀
# ░▒█▄▄▀░▒█░▒█░▒█▄▄▀░█▄▄█░█▄▄░░░░░░░░▒█▄▄▄░▒█░░▒█░▄█▄░▒█▄▄▄█░▒█▄▄▄█░▒█░▒█

# ---------------------------------------------------------------------------------------------
def menu():
    print("\n---------- CRC32 EMISOR ----------\n")
    trama = 0

    while True:
        trama = input("Ingrese una trama en binario: ")

        # eliminar espacios
        trama = trama.replace(" ", "")

        # Revisar que la trama sea binaria (solo tenga 0s y 1s)
        if not trama.isnumeric() or not all([int(i) in [0, 1] for i in trama]):
            print("La trama debe ser binaria (solo 0s y 1s)")
            continue

        else:
            break

    return trama

# P(x) = x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1
def crc32(trama):
    # 111011011011100010000011001000001
    polinomio = [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    SIZE = 32
    data = [int(bit) for bit in trama]  # Convert the trama to a list of integers

    # Agregar ceros al final de la trama
    data += [0] * SIZE

    # Valores a utilizar
    data_calc = data[0:len(polinomio)]
    data = data[len(polinomio):]

    # polinomio | data
    while True:
        # Se eliminan los bits no significativos
        eliminados = 0
        while data_calc[0] == 0:
            data_calc.pop(0)
            eliminados += 1

        # Se agregan los bits a data_calc para que sea del mismo tamaño que el polinomio
        for i in range(eliminados):

            # Si ya no hay bits en data, se termina el proceso
            if len(data) == 0:
                break

            else:
                bit = data.pop(0)
                data_calc.append(bit)

        # Si datacalc es menor que el polinomio, se termina el proceso
        if len(data_calc) < len(polinomio):
            
            # Si ya no hay bits en data, se termina el proceso
            if len(data) == 0:
                # Se agregan 0 al inicio de data_calc para que sea del mismo tamaño que el polinomio
                for i in range(SIZE - len(data_calc)):
                    data_calc.insert(0, 0)
                break

        # Si datacalc es igual al polinomio, se hace XOR entre ambos
        if len(data_calc) == len(polinomio):
            for i in range(len(polinomio)):
                data_calc[i] ^= polinomio[i]
            
        #print("XOR RESULT","".join([str(bit) for bit in data_calc]))

    # Convert the result back to a string representation
    crc = "".join([str(bit) for bit in data_calc])
    data_crc = trama + crc

    return data_crc


# ---------------------------------------------------------------------------------------------
trama = menu()
encoded = crc32(trama)
print("\nTrama codificada: " + encoded + "\n")


# ---------------------------------------------------------------------------------------------
# REFERENCIAS:
# 1. Polinomio de CRC3: https://en.wikipedia.org/wiki/Cyclic_redundancy_check#CRCs_and_data_integrity
# 2. Algoritmo Explicado por Jorge Yass: https://miro.com/app/board/uXjVMy_j06Y=/
# 3. Modulo CRC32: https://www.geeksforgeeks.org/modulo-2-binary-division/