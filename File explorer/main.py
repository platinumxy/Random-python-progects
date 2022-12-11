import os
import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk
from winreg import (HKEY_LOCAL_MACHINE, ConnectRegistry, HKEYType, OpenKey,
                    QueryValueEx)
from math import floor
from datetime import datetime

if os.name == "nt":
    import win32api, win32con, pywintypes

class ExtensionQuery:
    def __init__(self):
        """creates the base key and conncets its self to the regestery"""
        self.base: str = r"SOFTWARE\Classes"
        self.reg: HKEYType = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

    def _getValueFromClass(self, classStr: str) -> str:
        """retreives the value of a key from the regestery"""
        path: str = fr"{self.base}\{classStr}"
        key: HKEYType = OpenKey(self.reg, path)
        valueTuple: tuple[str, int] = QueryValueEx(key, "")
        return valueTuple[0]

    def getApplicationName(self, ext: str) -> str:
        """returns the file name by returning the value of the key from the regestry"""
        if not ext :
            return "Folder"
        try: 
            return self._getValueFromClass(self._getValueFromClass(ext))
        except FileNotFoundError:
            return f"{ext.removeprefix('.')} File"
        
    def __call__(self, ext: str) -> str:
        """Allias for self.getApplticationName"""
        return self.getApplicationName(ext)


#Creates file constants 
USERP = os.environ["USERPROFILE"]
APPDATAP = os.environ["APPDATA"]
ROOT = os.environ["SYSTEMDRIVE"]
getFileExtentionName:ExtensionQuery = ExtensionQuery()

class DefaultWindow:...#to stop syntax error from ide

class _BaseWindow:
    NAME = "Window"
    SIZE = "700x500"
    def __init__(self, path: str, parent: DefaultWindow = None) -> None:
        self.root = self.setup() if parent is None else parent._frame
        self.active = path
        self.showPage()
        self._refresh()
    
    def mainloop(self):
        self.root.mainloop()

    def setup(self):
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", exit)
        root.title(self.NAME)
        root.geometry(self.SIZE)
        return root
    
    def showPage(self):...
    def _refresh(self):...


class folderExplorer(_BaseWindow):
    def __init__(self, path: str, parent: DefaultWindow = None) -> None:
        super().__init__(path, parent)
        self.itemSelected = False
    def showPage(self):
        if not hasattr(self, "_pathBox"):
            self.row = 0
            self.pathBar()
            self.showTreeBox()
            
            self.AddFuncButton("Create Folder",print)
            self.AddFuncButton("Create File",print)
            self.AddFuncButton("Delete Selected",self.deleteSelected)
            self.AddFuncButton("Rename Selected","Re Select")
            self.AddFuncButton("Open Selected",self.openSelected)
            
        self.updateVars()

    def AddFuncButton(self,text:str,command):
        ttk.Button(self.root, text=text, command=lambda:command()).grid(row=self.row, column=4)
        self.row+=1

    def deleteSelected(self):
        try: 
            selection = self.active + "\\"+self.treeBox.item((self.treeBox.selection()))["values"][0]
        except IndexError:
            return
        if mb.askyesnocancel("Delete Selected", "Are you sure you want to delete\n"+selection):
            try: 
                os.remove(selection)
                self.updateVars()
            except PermissionError :
                mb.showerror("Permissions Error", "Unable to delete file as permissions are to low")
            except Exception as err:
                mb.showerror("Error deleting file",f"issue deleting file \n{err}")

    def openSelected(self):
        try: 
            selection = self.active + "\\"+self.treeBox.item((self.treeBox.selection()))["values"][0]
        except IndexError:
            return
        if os.path.isdir(selection):
            self.updatePath(fromTB=True)
            return 
        if getFileType(selection)[1] in inProgramEditors:
            try : #checks for parient class
                    mainWin = self.root.master
                    mainWin.changeFrame = {
                        "type": 'openFile',
                        "path": selection,
                        "oldPath": self.active
                    }
            except Exception:
                fileActions["openFile"](selection)
            return
        if mb.askyesno("Open File", "Open file in external program"):
            os.startfile(selection)
              

    def showTreeBox(self):
        tbColumns = ("file_name","file_type","creation_time","last_modified","file_size")
        self.treeBox = ttk.Treeview(self.root, columns=tbColumns, show="headings")
        self.treeBox.heading('file_name', text='Name')
        self.treeBox.heading('file_type', text='Type')
        self.treeBox.heading('creation_time', text='Date Created')
        self.treeBox.heading('last_modified', text='Date Modified')
        self.treeBox.heading('file_size', text='Size')
        self.treeBox.bind("<Return>", lambda*event: self.openSelected())
        self.treeBox.grid(row=self.row, column=0, columnspan=2, rowspan=10)
        ttk.Scrollbar(self.root, orient="vertical", command=self.treeBox.yview).grid(row=self.row, column=3, rowspan=10, ipady=100)
        self.row+=1
        
    def pathBar(self):
        ttk.Button(self.root, text="❰", command=self.upDir).grid(row=self.row, column=0)
        
        self.pathBox = tk.StringVar(self.root, self.active)
        self._pathBox = ttk.Entry(self.root, textvariable=self.pathBox)
        self._pathBox.bind("<Return>", lambda *any: self.updatePath(updateFromInput=True), )
        self._pathBox.grid(row=self.row, column=1, columnspan = 3, pady=1,ipadx=200)
        self.row += 1 
        ttk.Separator(self.root, orient='horizontal').grid(row=self.row, column=0, columnspan = 5, ipadx=400,pady=5)
        self.row += 1 
    
    def updatePath(self, *, updateFromInput: bool = False, newpath: str = "", fromTB:bool=False):
        if updateFromInput:
            if os.path.isdir(newpath := self.pathBox.get().removesuffix("\\")): 
                self.oldActive = self.active
                self.active = newpath
            elif os.path.isfile(newpath):
                try : #checks for parient class
                    mainWin = self.root.master
                    mainWin.changeFrame = {
                        "type": 'openFile',
                        "path": newpath,
                        "oldPath": self.active
                    }
                except Exception:
                    fileActions["openFile"](newpath)  
            else : 
                mb.showerror("Invalid Path", "Cannot open specified path")
                self.pathBox.set(self.active)
                return
        else:
            if fromTB:
                newpath = self.active + "\\"+self.treeBox.item((self.treeBox.selection()))["values"][0]
            self.oldActive = self.active
            self.active = newpath
            self.pathBox.set(self.active)
        self.showPage()
    
    def updateVars(self):
        self.treeBox.delete(*self.treeBox.get_children())
        try: 
            for file in fileAndFoldersInPath(self.active+"\\" if self.active[-1]==":" else self.active) : #acount for drives
                self.treeBox.insert('', tk.END, values=(file["FULLNAME"], file["EXTENTION NAME"], file["CREATION DATE"], file["MODIFICATION DATE"], (file["ROUNDED SIZE"] if file["TYPE"] == "FILE" else "")))
        except NotADirectoryError:
            mb.showerror("FIlE ERROR",f"Windows does not recognise file path\n{self.active}")
            self.active = self.oldActive 
            self.pathBox.set(self.active)
            self.updateVars()
            
    def upDir(self):
        if len(newpath := self.active.split("\\")) <= 1: 
            return
        self.updatePath(newpath="\\".join(newpath[:-1]))

class DefaultWindow(tk.Tk):
    def __init__(self, startingDir=USERP):
        super().__init__()
        self._frame = ttk.Frame()
        self._frame.pack()
        self.changeFrame:dict = {} 
        folderExplorer(path=startingDir, parent=self)
        self._refresh()
    
    def _refresh(self):
        if self.changeFrame:
            """change Frame layout
            {
                type:['openFile', 'openDir']
                path:(path)
                }
                """
                
            fileActions[self.changeFrame["type"]](path=self.changeFrame["path"], parent=self)
            self.changeFrame = {}    
        self.after(10, self._refresh)

def getFileType(file) -> tuple[str, str]:
    """Returns the file name and extention

    Args:
        file (str): The path to the requested file i.e. C:\\test\\Test.exe
        returns C:\\test\\Test, .exe

    Returns:
        tuple(FILENAME, .FILE EXTENTION) 
    """
    return os.path.splitext(file)

def openFileWithSytem(file:str) -> bool:
    try :
        with open(file) : pass 
        os.startfile(file)
        return True 
    except PermissionError :
        mb.showerror("Could not open file", f"Was unable to open\n'{file}'\nBecause you do not have permition to access this file\nTry running this program as administrator to bipass this")
    except Exception  as error:
        mb.showerror("Could not open file", f"Was unable to open\n'{file}'\nBecause {error}")
    return False

def getFileSize(pathToFile:str)-> tuple[int,str]:
    fileSizeMagnetude = {0:"B",10:"Kb",20:"Mb",30:"Gb",40:"Tb"}
    trueSize = os.path.getsize(pathToFile)
    for powerofTen in range(10,60,10):
        if trueSize/(2**powerofTen)<10: 
            return trueSize, f"{round(trueSize/(2**(powerofTen-10)))} {fileSizeMagnetude[powerofTen-10]}"

# TODO Add show hidden funculanlity, to do TOFIX \\.foo file showing as dir
def fileAndFoldersInPath(path: str, showHidden=False) -> list[dict]:
    """Returns information on all of the files and folders in a provided folder
    
    Args:
        path (str): The path to the folder you want to scan 

    Returns:
        list[dict]: list of all files in the dir in dicts which contain the file's NAME, TYPE(FILE/FOLDER) and PATH
    """
    def fType(path):
        fType = getFileType(path)
        return (" ​", fType) if isinstance(fType,str) else fType

    return [
        {
            "NAME": (fileAndExtent := fType(path+"\\"+file))[0],
            "FULLNAME":file,
            "EXTENTION":fileAndExtent[1],
            "EXTENTION NAME":getFileExtentionName(fileAndExtent[1]),
            "TYPE": ("FOLDER" if os.path.isdir((path + "\\" + file)) else "FILE"),
            "TRUE SIZE": getFileSize(path+"\\"+file)[0], 
            "ROUNDED SIZE": getFileSize(path+"\\"+file)[1],
            "CREATION DATE":datetime.fromtimestamp(os.path.getctime(path+"\\"+file)).strftime("%d/%m/%y %H:%M"),
            "MODIFICATION DATE":datetime.fromtimestamp(os.path.getmtime(path+"\\"+file)).strftime("%d/%m/%y %H:%M"),
            "PATH":path+"\\"+file
            } 
        for file in os.listdir(path) if not fileIsHidden(path+"\\"+file)]

def isPathFileOrFolder(path):
    return 

def fileIsHidden(path:str) -> bool:
    if os.name != "nt":
        return path.startswith('.')
    try :
        atter = win32api.GetFileAttributes(path)
    except pywintypes.error:
        return True
    return atter & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    
fileActions = {
    "openDir": folderExplorer,
}
inProgramEditors = {
    ".txt"
}
if __name__ == "__main__":
    #openFileWithSytem("C:\\DumpStack.log")
    dw = DefaultWindow()
    dw.mainloop()
    #TODO see if fil

