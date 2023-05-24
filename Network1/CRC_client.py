import socket


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
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# подключение
host = "localhost"
port = 9999
client_socket.connect((host, port))
print("Connected to server:", (host, port))

# Отправка на сервер
data = "10100010001100"
client_socket.send(data.encode())
print("Sent data to server:", data)

# Получение данных
crc_code = client_socket.recv(1024).decode()
print("Received CRC code from server:", crc_code)

# Проверка на ошибку
control = crc(data, "10011")
print(f"EXPECT {control}")
check = crc(data + crc_code, "10011")
print(f"crc {crc_code}")
if str(control) == str(crc_code):
    print("No errors detected in the data transmission.")
else:
    print("Errors detected in the data transmission.")

# close the socket
client_socket.close()
