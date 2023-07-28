def calcRedundantBits(m):
    # Hamming code logic to calculate the number of redundant bits needed
    for i in range(m):
        if (2**i >= m + i + 1):
            return i

def posRedundantBits(data, r):
    # Hamming code logic to insert redundant bits at their positions
    j = 0
    m = len(data)
    res = ''
    for i in range(1, m + r + 1):
        # Insert '0' at positions that are powers of 2
        if (i == 2**j):
            res = res + '0'
            j += 1
        else:
            res = res + data[-1]
            data = data[:-1]  # Remove last character from data
    return res[::-1]

def calcParityBits(arr, r):
    # Hamming code logic to calculate parity bits
    n = len(arr)
    for i in range(r):
        val = 0
        for j in range(1, n + 1):
            if (j & (2**i) == (2**i)):
                val = val ^ int(arr[-1 * j])
        arr = arr[:n - (2**i)] + str(val) + arr[n - (2**i) + 1:]
    return arr

# Enter the data to be transmitted
data = '1011001'

# Calculate the number of Redundant Bits Required
m = len(data)
r = calcRedundantBits(m)

# Determine the positions of Redundant Bits and add them to the data
arr = posRedundantBits(data, r)

# Determine the parity bits
arr = calcParityBits(arr, r)

# Data to be transferred
print("Data transferred is " + arr)
