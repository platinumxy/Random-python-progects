import tkinter as tk
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import tkinter.filedialog as FDialog
from dataclasses import dataclass, field
from functools import cache
from math import floor
from os import _exit
from random import choice
from threading import Thread
from time import sleep, time

from IMEallWords import ALLWORDS


@dataclass
class Monkey:
    name: str = "Monkey"
    running:bool = True
    words: list[str] = field(default_factory=list)
    largestWord = ""
    lenLargestWord = 0
    numWords = 0
    dead = False
    startTime = time()
    
    def __iter__(self) -> object :
        return self

    def __next__(self) -> str:
        if hasattr(self, "loopCount"):
            self.loopCount = self.loopCount + 1
        else:
            self.loopCount = 0
        if self.loopCount == len(self.words):
            del self.loopCount
            raise StopIteration
        return self.words[self.loopCount]
    
    def _updateVars(self) -> None:
        self.numWords = 0
        for word in self.words:
            if word == "":
                self.words.remove("")
                continue
            if len(word)>self.lenLargestWord:
                self.largestWord = word
                self.lenLargestWord = len(word)
            self.numWords = self.numWords + 1
            
    def guessWord(self, endlesslyGuess=True) -> None:
        """Guesses a word endlessly and adds it to the monkeys words"""

        # runs the code once then checks for endless run and if it is run forever as python does not have a REPEAT/DO .. UNTIL loop
        while True:
            if self.running:
                currentW, currentL = "", ""

                while currentL != " ":
                    currentL = choice(ALLLETTERS)
                    currentW = currentW + currentL
                if currentwInALLW(currentW):
                    self.addWordToWords(currentW[:-1])

                if not endlesslyGuess:
                    break
                
                #To force the thread to give up the GIL
                sleep(0.00001)
                if self.dead :
                    return
            else: 
                if self.dead :
                    return 
                sleep(1)

    def addWordToWords(self, word) -> None:
        self.words.append(word)
        self.numWords = self.numWords + 1
        if len(word) > self.lenLargestWord:
            self.largestWord = word
            self.lenLargestWord = len(word)


class HowManyMonkeys:
    """Creates a pop up box that sets numberOfMonkeys to the input"""
    def __init__(self, ) -> None:
        self.mainWin = tk.Tk()
        self.mainWin.title('How many monkeys?')
        self.mainWin.geometry('262x120')
        self.mainWin.resizable(False, False)
        self.mainWin.protocol("WM_DELETE_WINDOW", self._exit)
        self.numMonk = tk.IntVar(value="")
        
        ttk.Label(self.mainWin, text="How Many Monkeys").grid(row=0, column=0, columnspan=2)
        ttk.Label(self.mainWin, text="(Recomended no more than 5 for weak PCs)").grid(row=1, column=0, columnspan=2)
        
        self.numMonkBox = ttk.Entry(self.mainWin, textvariable=self.numMonk)
        self.numMonkBox.grid(row=2, column=0 ,ipady=5,pady=5, columnspan=2)
        self.numMonkBox.bind("<Return>", func=self._submit)
        self.numMonkBox.focus_set()
        
        self.sumbitButton = ttk.Button(self.mainWin, command=self._submit)
        self.sumbitButton.grid(row=3,column=0,ipady=3)
        
        ttk.Button(self.mainWin,text="Load From Save", command=self._loadFromFile).grid(row=3, column=1, ipady=3)

        self._updateButton()
        
    def _updateButton(self):
        """Endlessly updates the submit button with the value in the input box every 10ms"""
        try: 
            self.sumbitButton.config(text="Submit ("+str(self.numMonk.get())+")")
        except tk.TclError:
            self.sumbitButton.config(text="Submit (  )")
        self.mainWin.after(10, self._updateButton)
        
    def _submit(self, *args):
        """Takes args as the bind method passes the key pressed and we dont need that info """
        global NUMOFMONKEYS
        try: 
            NUMOFMONKEYS = int(self.numMonk.get())
            if NUMOFMONKEYS < 1 :
                return
        except:
            return
        self._exit(quietExit=True)
    
    def _exit(self, *, quietExit=False):
        if not quietExit :
            if mb.askyesno("Infinite Monkey Experiment", "Are you sure you want to quit?") :
               _exit(0)
            else: 
                return 
        else :
            self.mainWin.destroy()
    
    def _loadFromFile(self):
        global saveFile, saveFileData
        saveFile = FDialog.askopenfilename(filetypes=[("Monkey Words Files","*.mw")])
        if saveFile: # Check that a file was given 
            with open(saveFile, "r") as sf:
                saveFileData = sf.read()
            self._exit(quietExit=True)
        else: 
            del saveFile

    def mainloop(self):
        self.mainWin.mainloop()
        

class MainWindowIME(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.startTime = time()
        self.timeSinceStart = 0
        self._maxMonkeysPerPage = 10
        self._refreshRate = 300

    
        self.titleFont = ('Arial', 20, 'bold')
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Arial', 11))
        self.style.configure('TButton', font=('Arial', 11))
        self.LabPaddy = {"padx":1, "pady":5}
        self.ArrowPaddy = {"pady":5}
        
        
        self._frame:ttk.Frame = None 
        self._currentFrameFunc = None 
        self._travelHis: list[list[function, tuple, dict]] = [] 
        
        
        self.menu = tk.Menu(self)
        
        self.FileMenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(menu=self.FileMenu, label="File")
        self.FileMenu.add_command(label="New ...", command=lambda:print("New"))
        self.FileMenu.add_command(label="Open ...", command=lambda:print("Open"))
        self.FMSaveCasscade = tk.Menu(self.FileMenu, tearoff=0 )
        self.FMSaveCasscade.add_command(label="Save As ...", command=lambda:print("Save as"))
        try :
            global saveFile
            saveFile
            self.FMSaveCasscade.add_command(label="Save", command=lambda:print("Save"))
        except NameError: pass 
        self.FileMenu.add_cascade(menu=self.FMSaveCasscade, label="Save")
        
        self.MonkeysMenu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(menu=self.MonkeysMenu, label="Monekys")
        self.pausedAll = tk.IntVar()
        self.MonkeysMenu.add_checkbutton(label="Pause All", command=lambda:pauseAllMonkeys(self),
                                                         variable=self.pausedAll)
        self.monkPriorty = tk.IntVar()
        self.MonkeysMenu.add_checkbutton(label="Focus Resources On Monkeys", command=self.changeRefreshRate,variable=self.monkPriorty)
        self.MonkeysMenu.add_command(label="Start New Monkey", command=lambda:startNewMonkey(self))
        self.MonkeysMenu.add_command(label="Show Random Monkey", command=lambda:showRandomMonkey(self))
        self.protocol("WM_DELETE_WINDOW", self._exit)
        self.title('Infinite monkey experiment')
        self.geometry('700x500')
        self.config(menu=self.menu)
        self.swapFrame(self.renderHomePage)
        self._refresh()
        
    def _refresh(self) -> None:
        
        #Important note all variables that might need updating start with a capital to differenchiate 
        if self._currentFrameFunc == self.renderHomePage: # would use match case however does not work for backwards compat
            self.NumWordsFound.config(text=str(numWords()))
            self.LargestWordFound.config(text=largestWord())
            self.numMonkLabel.config(text=str(len(monkeyThreads)))
            
        elif self._currentFrameFunc == self.renderAllMonkeyData:
            for monkData in self.monkeysOnDisplay:
                monk = monkeys[monkData[0]]
                if monk.running  :
                    monkData[1].config(text="Active")
                else: 
                    monkData[1].config(text="Inactive")
                monkData[2].config(text=monk.largestWord)
                monkData[3].config(text=str(monk.numWords))
    
        elif self._currentFrameFunc == self.renderSpecificMonkeyInfo:
            for item in self.MonkeyListBox.get_children():
                self.MonkeyListBox.delete(item)
            for word in self.ActiveMonkey.words:
                self.MonkeyListBox.insert('', tk.END, values=(word,)) 
            self.SMNumWordsFound.config(text=str(self.ActiveMonkey.numWords))    
            self.TimeSinceMonkeyCreation.config(text=str(floor(time()-self.ActiveMonkey.startTime-2)))   
            self.LWFound.config(text=self.ActiveMonkey.largestWord)
            if self.ActiveMonkey.running:
                self.MonkeyStatus.config(text="Active")
            else:
                self.MonkeyStatus.config(text="Inactive")
                                                       
        self.timeSinceStart = time() - self.startTime
        self.TimeSSLabel.config(text=str(floor(self.timeSinceStart)))
        self.after(self._refreshRate, self._refresh)

    def _stopMRunning(self,activeM:Monkey,button:ttk.Button):
        activeM.running=False
        button.config(text="Resume", command=lambda: self._startMRunning(activeM,button))
    
    def _startMRunning(self,activeM:Monkey,button:ttk.Button):
        if self.pausedAll.get() :
            self.pausedAll.set(0)
        activeM.running=True
        button.config(text="Pause", command=lambda: self._stopMRunning(activeM,button))

    def _exit(self) -> None: 
        global saveFile
        try:
            save = mb.askyesnocancel("Save Words", f"Save changes to :\n{saveFile}")
        except NameError : 
            save = mb.askyesnocancel("Save Words", "Save the monkeys and their words?")
        if save == None:
            return
        if save :
            Exit = self._save()
            if not Exit:
                return
        _exit(0)      

    def _save(self) -> bool:
        global monkeys, monkeyThreads, saveFile
        
        def textFromMonkey(monkey:Monkey): return monkey.name+"|"+str(monkey.running) + "|" + "|".join(monkey.words) + "\n"
        
        FileExtentions = [("Monkey Words","*.mw"),("All Files","*.*")]
        
        try:
            (open(saveFile, "r")).close()
            _file = saveFile
        except Exception as error:
            if not isinstance(error, NameError):
                mb.showerror((type(error).__name__), str(error))
                return self._save()
            
            _file = FDialog.asksaveasfile(filetypes=FileExtentions,defaultextension=FileExtentions)
            if _file == None:
                return False
            else: 
                _file = _file.name
        for monkey in monkeys : 
            monkey.dead = True 
        
        with open(_file, "w") as file :
            textToPrint=[textFromMonkey(monkey) for monkey in monkeys]
            textToPrint[-1] = textToPrint[-1].removesuffix("\n") # removes the extra \n from the last monkey
            file.writelines(textToPrint)

        return True

    def changeRefreshRate(self):
        if self.monkPriorty.get(): self._refreshRate = 2000
        else: self._refreshRate = 300
            

    def swapFrame(self, render,*, _dontAddToBackLog=False, refresh=False, destroyerFunc=lambda *ANY: None, args:tuple=(), kwargs:dict={}) -> None :
        """Swaps the current _frame for the frame created with the given function

        Args:
            render (function): The frame renderer that you wish to use
            _dontAddToBackLog (bool, optional): States if the function should be added to the back stack. Defaults to False.
            refresh (bool, optional): If you are refreshing the page as otherwise the code will ignore it as its the same function. Defaults to False.
            destroyerFunc (function, optional): An optional function to be run before the frame is next changed, can be used to destroy frame specific vars. Defaults to lambda *args: None.
            args (tuple, optional): any args you want to pass the render. Defaults to ().
            kwargs (dict, optional): any kwargs you want to pass the render. Defaults to {}.
        """
        if isinstance(render, list): 
            render, args, kwargs = render
        if (self._currentFrameFunc == render) and (not refresh):
            return
        if self._frame != None :
            if not refresh :
                self.destroyerFunc()
                self.destroyerFunc = destroyerFunc
            self._frame.destroy()
            if (not _dontAddToBackLog) and (not refresh) :
                self._travelHis.append([self._currentFrameFunc,args,kwargs])
        else:
            self.destroyerFunc = destroyerFunc
        self._currentFrameFunc = render
        self._frame = ttk.Frame()
        self._frame.pack()
        render(*args, **kwargs)

    def renderHomePage(self, *args, **kwargs) -> None:
        ttk.Label(self._frame, text="The Infinite Monkey Experiment", font=self.titleFont).grid(row=0, column=0, columnspan=3, pady=20)
        
        
        ttk.Label(self._frame, text="Number of monkeys").grid(row=1, column=0, pady=10)
        ttk.Label(self._frame, text= "➤").grid(row=1, column=1, pady=10)
        self.numMonkLabel = ttk.Label(self._frame, text=str(len(monkeyThreads)))
        self.numMonkLabel.grid(row=1, column=2, padx=self.LabPaddy["padx"], pady=10)
        
        ttk.Label(self._frame, text="Num words found").grid(row=2, column=0, **self.ArrowPaddy)
        ttk.Label(self._frame, text= "➤").grid(row=2, column=1, **self.ArrowPaddy)
        self.NumWordsFound = ttk.Label(self._frame)
        self.NumWordsFound.grid(row=2, column=2, **self.LabPaddy)
        
        ttk.Label(self._frame, text="Largest word found").grid(row=3, column=0, **self.ArrowPaddy)
        ttk.Label(self._frame, text= "➤").grid(row=3, column=1, **self.ArrowPaddy)
        self.LargestWordFound = ttk.Label(self._frame)
        self.LargestWordFound.grid(row=3, column=2, **self.LabPaddy)


        ttk.Button(self._frame, text="See All Monkeys", command=lambda: self.swapFrame(self.renderAllMonkeyData,destroyerFunc=self.delRenderAllMonkeyData)).grid(row=4, column=0, columnspan=3)
        
        self.BackHomeTimeSinceStart(row=5, columnSpan=3)
    
    def renderAllMonkeyData(self, *args, **kwargs) -> None:
        self.pauseResumeB = []
        #to force the destroyer function to be the correct function so when entering this function from the back button otherwise it wont run
        self.destroyerFunc = self.delRenderAllMonkeyData
        def monkeyInfo(row,i):
            self.monkeysOnDisplay.append([i])
            self.monkeysOnDisplay[-1].append(ttk.Label(self._frame))
            self.monkeysOnDisplay[-1].append(ttk.Label(self._frame))
            self.monkeysOnDisplay[-1].append(ttk.Label(self._frame))
            
            ttk.Label(self._frame, text=monkeys[i].name).grid(row=row, column=0)
            self.monkeysOnDisplay[-1][1].grid(row=row,column=1)
            self.monkeysOnDisplay[-1][2].grid(row=row,column=2)
            self.monkeysOnDisplay[-1][3].grid(row=row,column=3) 
            
            ttk.Button(self._frame, text="More Info", command=lambda:self.swapFrame(self.renderSpecificMonkeyInfo, destroyerFunc=self.delRenderSpecificMonkeyInfo,args=(monkeys[i],))).grid(row=row, column=4)
            self.pauseResumeB.append(ttk.Button(self._frame))
            if monkeys[i].running :
                self.pauseResumeB[-1].config(text="Pause", command=lambda: self._stopMRunning(monkeys[i], self.pauseResumeB[-1]))
            else:
                self.pauseResumeB[-1].config(text="Resume", command=lambda: self._startMRunning(monkeys[i],self.pauseResumeB[-1]))
            self.pauseResumeB[-1].grid(row=row, column=5)
            ttk.Button(self._frame, text="Delete", command=lambda: self.deleteMonkey(monkeys[i], self.refreshAllMonkData)).grid(row=row, column=6)

        if not hasattr(self, "numMonkAlreadyLoaded"): 
            self.numMonkAlreadyLoaded = 0
        row = 0
        ttk.Label(self._frame, text="All Monkey Info Page", font=self.titleFont).grid(row=row,column=0, columnspan=7 )
        row = row+1 
        
        ttk.Label(self._frame, text="Monkey Name").grid(row=row, column=0, padx=4, pady=5)
        ttk.Label(self._frame, text="Status").grid(row=row, column=1, padx=4, pady=5)
        ttk.Label(self._frame, text="Largest Word").grid(row=row, column=2, padx=4, pady=5)
        ttk.Label(self._frame, text="Num Words").grid(row=row, column=3, padx=4, pady=5)
        
        row=row+1
        self.monkeysOnDisplay:list[list[int ,ttk.Label, ttk.Label, ttk.Label]] = []
        for i in range(self.numMonkAlreadyLoaded,
                       self._maxMonkeysPerPage+self.numMonkAlreadyLoaded):
            if i >= len(monkeys):
                break
            else: 
                self.numMonkAlreadyLoaded = self.numMonkAlreadyLoaded + 1
            monkeyInfo(row, i)
            
            row = row+1  
        
        newMonkBut = ttk.Button(self._frame, text="Create New Monkey", command=lambda: self.createNewMonkey(self.refreshAllMonkData))
        if self.numMonkAlreadyLoaded < len(monkeys):
            newMonkBut.grid(row=row, column=0, columnspan=3)
            ttk.Button(self._frame, text="More Monkeys", 
                       command=lambda:self.swapFrame(self.renderAllMonkeyData, destroyerFunc=self.delRenderAllMonkeyData, refresh=True)
                       ).grid(row=row, column=5, columnspan=3)
        else:
            newMonkBut.grid(row=row, column=0, columnspan=7)
        row=row+1 
        self.BackHomeTimeSinceStart(row=row, columnSpan=7)
    
    def delRenderAllMonkeyData(self) -> None:
        del self.numMonkAlreadyLoaded, self.monkeysOnDisplay
    
    def refreshAllMonkData(self):
        if self.numMonkAlreadyLoaded%self._maxMonkeysPerPage == 0:
            self.numMonkAlreadyLoaded = self.numMonkAlreadyLoaded - self._maxMonkeysPerPage
        else:
            self.numMonkAlreadyLoaded = self.numMonkAlreadyLoaded - (self.numMonkAlreadyLoaded%self._maxMonkeysPerPage)
        
        self.swapFrame(self.renderAllMonkeyData, refresh=True, destroyerFunc=self.delRenderAllMonkeyData)
    
    def renderSpecificMonkeyInfo(self, _monkey:Monkey=None) -> None: 
        def sortMwords(_monkey:Monkey) :
            _monkey.words.sort()
        row = 0
        self.ActiveMonkey = _monkey
        ttk.Label(self._frame, text=f"{_monkey.name}'s Info", font=self.titleFont).grid(row=row, column=0, columnspan=5)
        row=row+1
        
        self.MonkeyListBox = ttk.Treeview(self._frame, columns="Words", show='headings')
        self.MonkeyListBox.heading("Words", text="Words")
        self.MonkeyListBox.grid(row=row, rowspan=8, column=0, columnspan=2)
        scrollbar = ttk.Scrollbar(self._frame, orient=tk.VERTICAL, command=self.MonkeyListBox.yview)
        self.MonkeyListBox.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=row,rowspan=8, column=2, ipady=90)
        row=row+1
        
        ttk.Label(self._frame, text="Number Of Words Found").grid(row=row, column=3)
        #set the values to be non so _refresh fills the text box in
        self.SMNumWordsFound = ttk.Label(self._frame)
        self.SMNWFValue = 0
        self.SMNumWordsFound.grid(row=row, column=4)
        row=row+1
        
        ttk.Label(self._frame, text="Longest Word Found").grid(row=row, column=3)
        self.LWFound = ttk.Label(self._frame, text=_monkey.largestWord)
        self.LWFound.grid(row=row, column=4)
        row=row+1
        
        ttk.Label(self._frame, text="Time Since Creation").grid(row=row, column=3)
        self.TimeSinceMonkeyCreation = ttk.Label(self._frame, text=str(floor(time()-_monkey.startTime-2)))
        self.TimeSinceMonkeyCreation.grid(row=row, column=4)
        row=row+1
        
        ttk.Label(self._frame, text="Status").grid(row=row, column=3)
        self.MonkeyStatus = ttk.Label(self._frame)
        self.MonkeyStatus.grid(row=row, column=4)
        row=row+1
        
        self.SwapMonkeyStatusB = ttk.Button(self._frame)
        self.SwapMonkeyStatusB.grid(row=row, column=3, columnspan=2)
        if self.ActiveMonkey.running: 
            self.SwapMonkeyStatusB.config(text="Pause", command=lambda: self._stopMRunning(self.ActiveMonkey, self.SwapMonkeyStatusB))
        else:
            self.SwapMonkeyStatusB.config(text="Resume", command=lambda: self._startMRunning(self.ActiveMonkey, self.SwapMonkeyStatusB))
        row=row+1
        
        ttk.Button(self._frame, text="Sort Words", command=lambda:sortMwords(_monkey)).grid(row=row,column=3,columnspan=2)
        row=row+1
        
        ttk.Button(self._frame, text="Delete Monkey", command=lambda: self.deleteMonkey(self.ActiveMonkey, refreshHandeler=self.refreshSpesMonkInfo)).grid(row=row, column=3, columnspan=2)
        row=row+1

        self.BackHomeTimeSinceStart(row=row)
    
    def refreshSpesMonkInfo(self):
        self.swapFrame(self.renderAllMonkeyData, _dontAddToBackLog=True, destroyerFunc=self.delRenderAllMonkeyData)    
    
    def delRenderSpecificMonkeyInfo(self) -> None:
        del self.ActiveMonkey
    
    def BackHomeTimeSinceStart(self, *, row, column=0, columnSpan=5,customHomeKwargs={}, customBackKwargs={"_dontAddToBackLog":True}) -> None: 
        self.Home = ttk.Button(self._frame, text="Home", command=lambda: self.swapFrame(self.renderHomePage, **customHomeKwargs))
        self.Back = ttk.Button(self._frame, text="Back", command=lambda: self.swapFrame(self._travelHis.pop(), **customBackKwargs))
        if columnSpan%2 == 0 :
            HCS = int(columnSpan/2)
            self.Home.grid(row=row, column=column, columnspan=HCS)
            self.Back.grid(row=row, column=column+HCS, columnspan=HCS)
        else : 
            HCS = floor(columnSpan/2)
            self.Home.grid(row=row, column=column, columnspan=HCS)
            self.Back.grid(row=row, column=column+1+HCS, columnspan=HCS)
        
        timeSS = ttk.Labelframe(self._frame, labelwidget=ttk.Label(text="Seconds Since Start", font=('Arial', 13)))
        timeSS.grid(row=row+1,column=column, columnspan=columnSpan)
        
        self.TimeSSLabel = ttk.Label(timeSS, text=str(self.timeSinceStart))
        self.TimeSSLabel.pack()
    
    def deleteMonkey(self, _monkey:Monkey, refreshHandeler= lambda *args, **kwargs: None, *,  refreshHArgs:tuple=(), refreshHKwargs:dict={}) -> None:
        if mb.askokcancel("Delete Monkey", f"Are you sure you wish to delete {_monkey.name}"):
            global monkeys, monkeyThreads
            mIndex = monkeys.index(_monkey)
            monkeys[mIndex].dead = True 
            monkeys.pop(mIndex)
            monkeyThreads.pop(mIndex)
            refreshHandeler(*refreshHArgs, **refreshHKwargs)            
        else: 
            return
        
    def createNewMonkey(self, refreshFunc, rFArgs:tuple=(), rFKwargs:dict={}, *args, **kwargs):
        global NUMOFMONKEYS, monkeyThreads, monkeys 
        NUMOFMONKEYS = NUMOFMONKEYS + 1 
        monkeys.append(Monkey(f"Monkey - {NUMOFMONKEYS}"))
        monkeyThreads.append(Thread(target=monkeys[-1].guessWord))
        monkeyThreads[-1].start()
        self.pausedAll.set(0)
        refreshFunc(*rFArgs,*args,**kwargs,**rFKwargs)
    
@cache
def currentwInALLW(word: str) -> bool:
    return word[:-1] in ALLWORDS

def numWords() -> int :
    total = 0 
    for monk in monkeys :
        total = total + monk.numWords
    return total 

def largestWord() -> str :
    BigWord =""
    for monk in monkeys:
        if monk.lenLargestWord > len(BigWord):
            BigWord = monk.largestWord
    return BigWord

def monkeyHandeler(numMonkeys: int) -> None:
    global monkeys, monkeyThreads
    
    if not ((hasattr(globals, "monkeys")) and (hasattr(globals, "monkeyThreads"))):
        monkeys, monkeyThreads = [], [] # make sure that the monekys and monkeyThreads exsist
    
    for monkeyNum in range(numMonkeys):
        monkeys.append(Monkey(f"Monkey - {monkeyNum+1}"))
        monkeyThreads.append(Thread(target=monkeys[-1].guessWord))
        monkeyThreads[-1].start()

def fromSaveMonkeyHandeler(fileInfo) -> None:
    """Format of MW file
    MonkeyName|MonkeyStatus|monkeysWord|monkeysWord
    MonkeyName|MonkeyStatus|monkeysWord|monkeysWord
    """
    global NUMOFMONKEYS, monkeys, monkeyThreads
    fileInfo = fileInfo.split("\n")
    NUMOFMONKEYS = len(fileInfo)
    for line in fileInfo:
        words = line.split("|")
        monkeys.append(Monkey(words[0], (words[1]=="True"), words[2:]))
        monkeys[-1]._updateVars()
        monkeyThreads.append(Thread(target=monkeys[-1].guessWord))
        monkeyThreads[-1].start()
    
def openNewMWFile(window:MainWindowIME):
    """Handles the User attempting to open a new file"""
    #needs 
    #pop up asking if wants to save (could latch onto save file, use empty except to catch _exit)
    #destroy window
    #recreate monkey from save 
    #re-create window

def newMonkeys(window:MainWindowIME):
    """Handles the user wanting to create a new set of monkeys"""
    #pop up asking if wants to save (could latch onto save file, use empty except to catch _exit)
    #Destroy all monekys 
    #Create Pop up box that asks how many moneyks 
    #Start that many monkeys 
    #Refresh all pages, and start time

def startNewMonkey(window:MainWindowIME):
    """Starts a new monkey from menu bar"""
    #Runs the add new monkey command, just ignores the refresh func if on home screen 
    if window._currentFrameFunc == window.renderAllMonkeyData:
        window.createNewMonkey(window.refreshAllMonkData)
    elif window._currentFrameFunc == window.renderSpecificMonkeyInfo:
        window.createNewMonkey(window.refreshSpesMonkInfo)
    else: 
        window.createNewMonkey(window._currentFrameFunc)
        
def pauseAllMonkeys(window:MainWindowIME):
    """Pauses all monkeys running"""
    global monkeys
    def buttonConfig(button, i, text, command):
        if window.numMonkAlreadyLoaded%window._maxMonkeysPerPage == 0:i = (window.numMonkAlreadyLoaded - window._maxMonkeysPerPage) + i
        else:i = (window.numMonkAlreadyLoaded - (window.numMonkAlreadyLoaded%window._maxMonkeysPerPage)) + i
        button.config(text=text, command=lambda: command(monkeys[i], button))
        
    if not (window.pausedAll.get()):
        for monkey in monkeys :
            monkey.running = True
        if window._currentFrameFunc == window.renderAllMonkeyData : 
            for i, button in enumerate(window.pauseResumeB): buttonConfig(window.pauseResumeB[i], i, "Pause", window._stopMRunning)
    else :
        for monkey in monkeys :
            monkey.running = False 
        if window._currentFrameFunc == window.renderAllMonkeyData:
            for i, button in enumerate(window.pauseResumeB): buttonConfig(window.pauseResumeB[i], i, "Resume", window._startMRunning)

def showRandomMonkey(window:MainWindowIME):
    """Takes the user to a random monkey page"""
    global monkeys 
    if not (window._travelHis):
        window._travelHis.append([window.renderHomePage,(),{}])
    window.swapFrame(window.renderSpecificMonkeyInfo, destroyerFunc=window.delRenderSpecificMonkeyInfo,args=(choice(monkeys),))

def main():
    global NUMOFMONKEYS
    NUMOFMONKEYS = 1
    HowManyMonkeys().mainloop()

    try: 
        global saveFile, saveFileData
        if saveFileData =="":
            mb.showerror("Error","Invalid File Selected")
            del saveFile, saveFileData
            main()
        Thread(target=fromSaveMonkeyHandeler, args=(saveFileData,)).start()
    except NameError:
        Thread(target=monkeyHandeler, args=(NUMOFMONKEYS,)).start()
    
    MainWindowIME().mainloop()
    
ALLLETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L','M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
SPACEFREQUENCY = 5
for _ in range(SPACEFREQUENCY): ALLLETTERS.append(' ')
#As type annotations cannot be declared as global inside of functions 
monkeys: list[Monkey] = []
monkeyThreads: list[Thread] = []



if __name__ == "__main__":
    main()
    #TODO add menu bar 