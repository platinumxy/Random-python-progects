import socket
import threading
import tkinter
from tkinter import messagebox
from time import sleep 

class Server(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title('Server')
        self.configure(background='#f0f0f0')
        self.protocol('WM_DELETE_WINDOW', lambda: self.Close())
        self.messages = ['host == '+socket.gethostname()] 
        self.DisplayMessages()

    def ClearPage(self): 
        for child in self.winfo_children(): child.destroy()

    def Close(self): 
        if messagebox.askyesno('Close', 'Are you sure you want to close?'): 
            self.destroy()
            from os import _exit
            _exit(0)


    def DisplayMessages(self):
        self.ClearPage()
        scrollbar = tkinter.Scrollbar(self)
        scrollbar.grid(row=0, column=3, sticky=tkinter.N+tkinter.S)
        Messages = tkinter.Listbox(self, yscrollcommand=scrollbar.set, width=100, height=20)
        scrollbar.config(command=Messages.yview)
        Messages.grid(row=0, column=0)
        for message in self.messages:
            Messages.insert(tkinter.END, message)

    def Refresh(self):
        updateted = False
        for index, item in enumerate(updated):
            if not item :
                continue
            updateted = True 
            self.messages.append(clients[index][-1])
            updated[index] = False
        if updateted:
            self.DisplayMessages()
    
                


def autoRefresher(func):
    while True :
        sleep(0.5)
        func()


def connectionsHandeler(clients,updated):
    global sock
    c, addr = sock.accept()
    print("Client connected", addr)
    clients.append([threading.Thread(target=clientHandeler, args=(c, addr, len(clients))), c, addr, f"Client connected {addr}"])
    updated.append(True)
    clients[-1][0].start()

def clientHandeler(c, addr, index):
    global updated, clients
    while True:
        try:
            content = c.recv(9999).decode()
            if not content:break
            updated[index] = True
            clients[index][-1] = f"{addr[0]} -> {addr[1]} {content}"
            print(content)
        except ConnectionResetError:
            break
    clients[index] = None 
    updated[index] = None 
    print("Client closed", addr)
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
