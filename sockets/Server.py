import socket
import threading


def clientHandeler(c, addr, index):
    while True:
        try:
            content = c.recv(300).decode()
            if not content:
                break
            print(f"{addr[0]} -> {addr[1]} : {content}")
        except ConnectionResetError:
            break
    clients.pop(index)
    print("Client connected", addr)
    return


clients = []

s = socket.socket()
host = socket.gethostname()
print(host)
port = 62_444
s.bind((host, port))
s.listen(0)
while True:
    c, addr = s.accept()
    print("Client connected", addr)
    clients.append((threading.Thread(target=clientHandeler, args=(
        c, addr, len(clients))), c, addr, len(clients)))
    clients[-1][0].start()


