import socket
import random

# Пораждающая и проверочная матрицы
G = [[1, 1, 0, 1, 0, 0, 0],
     [0, 1, 1, 0, 1, 0, 0],
     [0, 0, 1, 1, 0, 1, 0],
     [0, 0, 0, 1, 1, 0, 1]]

H = [[1, 0, 1, 1, 1, 0, 0],
     [0, 1, 0, 1, 1, 1, 0],
     [0, 0, 1, 0, 1, 1, 1]]


# Define a function to introduce a random error into a code word
# Добавляем случайную ошибку
def introduce_error(code_word):
    n = len(code_word)
    i = random.randint(0, n - 1)
    code_word[i] = (code_word[i] + 1) % 2
    return code_word


# Сокет для подключения
s = socket.socket()

host = ""
port = 9999

s.bind((host, port))
# Ждём подключения
s.listen(1)
print("Wait for connect")
# Пришло подключение
conn, addr = s.accept()
print('Connected by', addr)
# Получаем сообшение
message = conn.recv(1024)
code_word = list(message)
print('Received message:', code_word)
#
# code_word = calculate_hamming_code(message)
# print('Code word:', code_word)
# Introduce a random error into the code word
code_word = introduce_error(code_word)
print('Code word with error:', code_word)
# Send the code word with error back to the client
conn.send(bytes(code_word))
# Close the connection
conn.close()
