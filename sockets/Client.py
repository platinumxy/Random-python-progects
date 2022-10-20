import socket

s=socket.socket()

host = input("Enter host name (default will be local machine)") 
if host == "":
    host=socket.gethostname() #server hostname
port=62_444 #same as server
s.connect((host,port))


while True :
    message = input("Enter the message you wish to send :\n")
    if message == "QUIT": break
    try :
        s.send(message.encode())
    except ConnectionResetError: 
        input("Connection was reset restart the program to try reconect")
        break
s.close()