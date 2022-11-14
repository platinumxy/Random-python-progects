import socket
import threading
import tkinter
from tkinter import messagebox as mb
from tkinter import ttk as ttk
from time import sleep, time
from collections import deque
from math import floor 
from plyer import notification

# Folowing code taken from folder and file handler see there for explaination and docs
def MoveTo(fileName:str) ->  str: return __RecursiveMoveTo(fileName, True)
def __RecursiveMoveTo(fileName, __START=False):
    from os import getcwd, listdir, chdir, path 
    cwd = getcwd()
    for file in listdir(cwd):
        if path.isfile(file): 
            if file == fileName:return cwd
        else :
            try :
                chdir(cwd+"\\"+file)
                found = __RecursiveMoveTo(fileName)
                if found : return cwd 
            except NotADirectoryError: pass 
    if __START :raise FileNotFoundError()
    else: return False 
#Used to avoid issues coming from IDEs not running code in correct folder 
AppIcon = "AppIcon.ico"
MoveTo(AppIcon)

class Server(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('Server')
        self.configure(background='#f0f0f0')
        self.protocol('WM_DELETE_WINDOW', lambda: self.Close())
        self.messages = deque(['host = '+socket.gethostname(),'Time Stamp - IP : Address -> Message'])
        self.DisplayMessages()

    def ClearPage(self): 
        for child in self.winfo_children(): child.destroy()

    def Close(self): 
        if mb.askyesno('Close', 'Are you sure you want to close?'): 
            self.destroy()
            from os import _exit
            _exit(0)


    def DisplayMessages(self):
        self.ClearPage()
        scrollbar = ttk.Scrollbar(self)
        scrollbar.grid(row=0, column=3, sticky=tkinter.N+tkinter.S)
        self.DMessages = tkinter.Listbox(self, yscrollcommand=scrollbar.set, width=100, height=20)
        scrollbar.config(command=self.DMessages.yview)
        self.DMessages.grid(row=0, column=0)
        for message in self.messages:
            self.DMessages.insert(tkinter.END, message)
        ttk.Button(self, text="SAVE", command=self.save).grid(row=1,column=0)

    def Refresh(self):
        for index, item in enumerate(updated):
            if not item :
                continue
            updateted = True 
            self.messages.append(clients[index][-1])
            self.DMessages.insert(tkinter.END, clients[index][-1])

            temp = clients[index][-1].split(" -> ")
            ip = temp[0].split("-")[1]
            content = temp[1]

            notification.notify(
                    title = ip,
    message = content,
    app_icon = AppIcon,
    timeout = 1,
            )


            updated[index] = False
    
    def save(self):
        with open("logs.log","w") as log:
            log.write("\n".join(self.messages))

def autoRefresher(func):
    while True :
        sleep(0.1)
        func()


def connectionsHandeler(clients,updated):
    global sock
    while True :
        c, addr = sock.accept()
        print("Client connected", addr)
        clients.append([threading.Thread(target=clientHandeler, args=(c, addr, len(clients))), c, addr, f"{floor(time())}-{addr[0]}:{addr[1]} -> Connected"])
        updated.append(True)
        clients[-1][0].start()

def clientHandeler(c, addr, index):
    global updated, clients
    while True:
        try:
            content = c.recv(9999).decode()
            if not content:break
            updated[index] = True
            clients[index][-1] = f"{floor(time())}-{addr[0]}:{addr[1]} -> {content}"
            print(content)
        except ConnectionResetError:
            break
    clients[index] = [f"{floor(time())}-{addr[0]}:{addr[1]} disconnected"] 
    updated[index] = None 
    
    return

if __name__ == '__main__':
    clients = []
    updated = []
    sock = socket.socket()
    host = socket.gethostname()
    print(host)
    port = 62_444
    sock.bind((host, port))
    sock.listen(0)

    app = Server()

    connectionsHandle = threading.Thread(target=connectionsHandeler,args=(clients,updated) )
    apploop = threading.Thread(target=app.mainloop)
    autoRefresh = threading.Thread(target=autoRefresher, args=(app.Refresh,))
    
    connectionsHandle.start()
    autoRefresh.start()
    app.mainloop()
