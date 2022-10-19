import socket

s=socket.socket()
host=socket.gethostname()
print(host)
port=62_444 
s.bind((host,port))
s.listen(10)
while True:
    c,addr=s.accept()
    print ("Client connected",addr)
    print ("Got Connection from" ,addr)
    content=c.recv(100).decode()
    if not content:
        break
    print (content)
print("Resived")