import socket
import random

## Пораждающая и проверочная матрицы
# G = [[1, 0, 0, 0, 1, 1, 1],
#     [0, 1, 0, 0, 1, 0, 1],
#     [0, 0, 1, 0, 1, 1, 0],
#     [0, 0, 0, 1, 0, 1, 1]]
#
# H = [[1, 1, 0, 1, 1, 0, 0],
#     [1, 0, 1, 1, 0, 1, 0],
#     [0, 1, 1, 1, 0, 0, 1]]
# Пораждающая и проверочная матрицы
G = [[1, 1, 0, 1, 0, 0, 0],
     [0, 1, 1, 0, 1, 0, 0],
     [0, 0, 1, 1, 0, 1, 0],
     [0, 0, 0, 1, 1, 0, 1]]

H = [[1, 0, 1, 1, 1, 0, 0],
     [0, 1, 0, 1, 1, 1, 0],
     [0, 0, 1, 0, 1, 1, 1]]


# Создаем слово
def generate_message(n):
    message = []
    for i in range(n):
        message.append(random.randint(0, 1))
    return message


def calculate_hamming_code(message):
    # Параметры кода
    k = len(message)
    r = len(G[0])
    n = k + r
    # Получаем кодовое слово умножением на порождающую матрицу
    code_word = []
    for i in range(r):
        s = 0
        for j in range(k):
            s += message[j] * G[j][i]
        code_word.append(s % 2)
    return code_word


# Define the client function
# Create a socket object
s = socket.socket()

host = "localhost"
port = 9999
# Подключаемся
s.connect((host, port))
# Создаем сообшение длины 4
message = generate_message(4)
print(f'Message: {message}')
# Отправка сообщения
code_word = calculate_hamming_code(message)
print(f"Hamming message {code_word}")
s.send(bytes(code_word))
# Получаем слово с ошибкой
code_word = s.recv(1024)
code_word = [int(bit) for bit in code_word]
print('Code word with error:', code_word)
# Ищем ошибку
syndrome = []
for i in range(len(H)):
    s = 0
    for j in range(len(code_word)):
        s += code_word[j] * H[i][j]
    syndrome.append(s % 2)
print('Syndrome:', syndrome)
if sum(syndrome) != 0:
    print("Error in word")
    # Поиск позиции ошибки
    for i in range(len(H[0])):
        if H[0][i] == syndrome[0]:
            if H[1][i] == syndrome[1]:
                if H[2][i] == syndrome[2]:
                    position = i
                    print('Error at position:', position)
                    code_word[position] = (code_word[position] + 1) % 2
                    print('Corrected code word:', code_word)
                    break

# Close the connection
