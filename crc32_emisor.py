# ░▒█▀▀▄░▒█▀▀▄░▒█▀▀▄░█▀▀█░█▀█░░░░░░░░▒█▀▀▀░▒█▀▄▀█░▀█▀░▒█▀▀▀█░▒█▀▀▀█░▒█▀▀▄
# ░▒█░░░░▒█▄▄▀░▒█░░░░░▒▀▄░▒▄▀░░░▀▀░░░▒█▀▀▀░▒█▒█▒█░▒█░░░▀▀▀▄▄░▒█░░▒█░▒█▄▄▀
# ░▒█▄▄▀░▒█░▒█░▒█▄▄▀░█▄▄█░█▄▄░░░░░░░░▒█▄▄▄░▒█░░▒█░▄█▄░▒█▄▄▄█░▒█▄▄▄█░▒█░▒█

# ---------------------------------------------------------------------------------------------
def menu():
    print("\n---------- CRC3 EMISOR ----------\n")
    trama = 0

    while True:
        trama = input("Ingrese una trama en binario: ")

        # Revisar que la trama sea binaria (solo tenga 0s y 1s)
        if not trama.isnumeric() or not all([int(i) in [0, 1] for i in trama]):
            print("La trama debe ser binaria (solo 0s y 1s)")
            continue

        else:
            break

    return trama
    
# P(x) = x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1
def crc32(trama):
    # 11101101101110001000001100100000
    polinomio = [int(bit) for bit in "11101101101110001000001100100000"]
    data = [int(bit) for bit in trama]  # Convert the trama to a list of integers
    flag = False

    # Agregar ceros al final de la trama
    data += [0] * 32
    data_calc = []

    # Operacion XOR
    while data != []:
        
        # Agregar valores de data a data_calc
        if not (len(data_calc) >= len(polinomio)):
            for i in range(len(polinomio) - len(data_calc)):
                if data == []:
                    break
                else:
                    a = data.pop(0)
                    data_calc.append(a)

        # XOR entre los elementos de polinomio y trama
        for i in range(len(polinomio)):

            if len(data_calc) == len(polinomio):
                a = data_calc[i]
                b = polinomio[i]

                data_calc[i] = a ^ b
            else:
                break

        # Eliminar los primeros ceros de la trama
        while data_calc[0] == 0 and data != []:
            data_calc.pop(0)

    # Seleccionar los primeros 3 bits de data_calc
    data_calc = data_calc[:32]

    # Convert the result back to a string representation
    crc = "".join([str(bit) for bit in data_calc])
    data_crc = trama + crc

    return data_crc


# ---------------------------------------------------------------------------------------------
trama = menu()
encoded = crc32(trama)
print("Trama codificada: " + encoded)


# ---------------------------------------------------------------------------------------------
# REFERENCIAS:
# 1. Polinomio de CRC3: https://en.wikipedia.org/wiki/Cyclic_redundancy_check#CRCs_and_data_integrity
# 2. Calculadora de CRC3 para pruebas: https://www.lammertbies.nl/comm/info/crc-calculation