import socket
import random


def crc(data, generator):

    dividend = data + "0" * (len(generator) - 1)
    divisor = generator
    remainder = ""

    for i in range(len(generator)):
        remainder += dividend[i]

    for i in range(len(generator), len(dividend)):
        if remainder[0] == "1":
            temp = ""
            for j in range(len(generator)):
                temp += str(int(remainder[j]) ^ int(divisor[j]))
            remainder = temp[1:] + dividend[i]
        else:
            remainder = remainder[1:] + dividend[i]

    return remainder


# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Указывааем ip и port
host = ""
port = 9999
server_socket.bind((host, port))

# Ждем подключение клиента
server_socket.listen(1)
print("Server is listening for connections...")

# Подключаем клиента
client_socket, client_address = server_socket.accept()
print(f"Connected to client: {client_address}")

# Получение данных от клиента
data = client_socket.recv(1024).decode()
print(f"Received data from client: {data}")

# Добавление ошибки
position = random.randint(0, len(data) - 1)
data = data[:position] + "1" + data[position + 1:]

print(f"Data with error:{data}")

# Создаем CRC код
generator = "10011"  # x^4 + x + 1
crc_code = crc(data, generator)

# send the CRC code back to the client
client_socket.send(crc_code.encode())

# close the socket
client_socket.close()
server_socket.close()
