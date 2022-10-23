import socket
from time import sleep, time
from threading import Thread

def MessageReciver():
    while True:
        try:
            mess = client.recv(300)
            if not mess:
                continue
            print("\n> "+mess.decode())
        except ConnectionResetError:
            try:
                Uhost
                input("The server disconnected restart the program to reconnect")
            except:
                input("The client disconnected restart the program to reconnect")
            exit()


def MessageSender():
    while True:
        message = input("- ")
        if message == "QUIT":
            break
        try:
            client.send(message.encode())
        except ConnectionResetError:
            try:
                Uhost
                input("The server disconnected restart the program to reconnect")
            except:
                input("The client disconnected restart the program to reconnect")
            exit()


def actAsServer():
    Uinput = ""
    while not ((Uinput == "s") or (Uinput == "c")):
        Uinput = input(
            "Act as a Server(s) or a Client (c)\n").lower().strip(" ")
    if Uinput == "s":
        return True
    return False

def waitingScreen():
    while True:
        print("Waiting for client to connect -", end="\r",)
        sleep(0.3)
        if found:
            break
        print("Waiting for client to connect \\", end="\r",)
        sleep(0.3)
        if found:
            break
        print("Waiting for client to connect |", end="\r",)
        sleep(0.3)
        if found:
            break
        print("Waiting for client to connect /", end="\r",)
        sleep(0.3)
    print("\nClient found")


s = socket.socket()
host = socket.gethostname()
port = 62_444 


if actAsServer():
    s.bind((host, port))
    s.listen(0)
    found = False
    Thread(target=waitingScreen).start()
    client, addr = s.accept()

else:
    Uhost = input("Enter host name (default will be local machine)")
    if Uhost != "":
        host = Uhost
    Stime = time()
    while True:
        try:
            if (time() - Stime) > 40:
                input("Server timed out")
                exit()
            s.connect((host, port))
            break
        except ConnectionRefusedError:
            pass
    client = s

Thread(target=MessageSender).start()
Thread(target=MessageReciver).start()
