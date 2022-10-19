import socket
import os

def MoveTo(fileName:str) ->  str: return __RecursiveMoveTo(fileName, True)
def __RecursiveMoveTo(fileName, __START=False):
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if os.path.isfile(file): 
            if file == fileName:return cwd
        else :
            try :
                os.chdir(cwd+"\\"+file)
                found = __RecursiveMoveTo(fileName)
                if found : return cwd 
            except NotADirectoryError: pass 
    if __START :raise FileNotFoundError()
    else: return False 

MoveTo("textToSend.txt")

s=socket.socket()

host = input("Enter host name (default will be local machine)") 
if host == "":
    host=socket.gethostname() #server hostname
port=62_444 #same as server


s.connect((host,port))
fileToSend = open("textToSend.txt","r")
content = fileToSend.read()
s.send(content.encode())
s.close()
input("Sent!")