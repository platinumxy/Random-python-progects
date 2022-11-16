import tkinter.messagebox as mb
import tkinter as tk
import tkinter.ttk as ttk
from time import sleep , time
from math import floor 
from os import _exit
from threading import Thread
from dataclasses import dataclass, field
from functools import cache
from random import choice
from allwords import ALLWORDS


@dataclass
class monkey:
    name: str = "Monkey"
    noPrint: bool = False
    words: list[str] = field(default_factory=list)
    largestWord = ""
    lenLargestWord = 0
    numWords = 0
    running = True

    def __iter__(self) -> object :
        return self

    def __next__(self) -> str:
        try:
            self.loopCount = self.loopCount + 1
        except AttributeError:
            self.loopCount = 0
        if self.loopCount == len(self.words):
            del self.loopCount
            raise StopIteration
        return self.words[self.loopCount]

    def guessWord(self, endlesslyGuess=True) -> None:
        """Guesses a word endlessly and adds it to the monkeys words"""

        # runs the code once then checks for endless run and if it is run forever as python does not have a REPEAT/DO .. UNTIL loop
        while True:
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

    def addWordToWords(self, word) -> None:
        if not self.noPrint:
            print(self.name, "found", word)
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
        self.mainWin.geometry('285x120')
        self.mainWin.resizable(False, False)
        self.mainWin.protocol("WM_DELETE_WINDOW", self._exit)
        self.numMonk = tk.IntVar(value="")     
        
        ttk.Label(self.mainWin, text="How Many Monkeys").pack()
        ttk.Label(self.mainWin, text="(Recomended no more than 10)").pack()
        
        self.numMonkBox = ttk.Entry(self.mainWin, textvariable=self.numMonk)
        self.numMonkBox.pack(ipady=5,pady=5)
        self.numMonkBox.bind("<Return>", func=self._submit)
        self.numMonkBox.focus_set()
        
        self.sumbitButton = ttk.Button(self.mainWin, command=self._submit)
        self.sumbitButton.pack(ipady=3)

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
            
    def mainloop(self):
        self.mainWin.mainloop()
        

class MainWindowIME(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.startTime = time()
        self.timeSinceStart = 0
        self._maxMonkeysPerPage = 10
        
        self.titleFont = ('Arial', 20, 'bold')
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Arial', 11))
        self.style.configure('TButton', font=('Arial', 11))
        self.LabPaddy = {"padx":1, "pady":5}
        self.ArrowPaddy = {"pady":5}
        
        self._frame:ttk.Frame = None 
        self._currentFrameFunc = None 
        self._travelHis: list[function] = [] 
        
        
        self.protocol("WM_DELETE_WINDOW", self._exit)
        self.title('Infinite monkey experiment')
        self.geometry('700x500')
        self.swapFrame(self.renderHomePage)
        self._refresh()
        
        
    def _refresh(self):
        
        #Important note all variables that might need updating start with a capital to differenchiate 
        if self._currentFrameFunc == self.renderHomePage:
            self.NumWordsFound.config(text=str(numWords()))
            self.LargestWordFound.config(text=largestWord())
            
        elif self._currentFrameFunc == self.renderAllMonkeyData:
            for monkData in self.monkeysOnDisplay:
                monk = monkeys[monkData[0]]
                if monk.running  :
                    monkData[1].config(text="Active")
                else: 
                    monkData[1].config(text="InActive")
                monkData[2].config(text=monk.largestWord)
                monkData[3].config(text=str(monk.numWords))
    
        self.timeSinceStart = time() - self.startTime
        self.TimeSSLabel.config(text=str(floor(self.timeSinceStart)))
        self.after(100, self._refresh)

    def _exit(self):
        _exit(0)

    def swapFrame(self, render,*, _dontAddToBackLog=False, refresh=False, destroyerFunc=lambda: _pass()) -> None :
        if (self._currentFrameFunc == render) and (not refresh):
            return
        if self._frame != None :
            destroyerFunc()
            self._frame.destroy()
            if (not _dontAddToBackLog) and (not refresh) :
                self._travelHis.append(self._currentFrameFunc)
                
        self._currentFrameFunc = render
        self._frame = ttk.Frame()
        self._frame.pack()
        render()

    def renderHomePage(self):
        ttk.Label(self._frame, text="The Infinite Monkey Experiment", font=self.titleFont).grid(row=0, column=0, columnspan=3, pady=20)
        
        
        ttk.Label(self._frame, text="Number of monkeys").grid(row=1, column=0, pady=10)
        ttk.Label(self._frame, text= "➤").grid(row=1, column=1, pady=10)
        ttk.Label(self._frame, text=str(len(monkeys))).grid(row=1, column=2, padx=self.LabPaddy["padx"], pady=10)
        
        ttk.Label(self._frame, text="Num words found").grid(row=2, column=0, **self.ArrowPaddy)
        ttk.Label(self._frame, text= "➤").grid(row=2, column=1, **self.ArrowPaddy)
        self.NumWordsFound = ttk.Label(self._frame)
        self.NumWordsFound.grid(row=2, column=2, **self.LabPaddy)
        
        ttk.Label(self._frame, text="Largest word found").grid(row=3, column=0, **self.ArrowPaddy)
        ttk.Label(self._frame, text= "➤").grid(row=3, column=1, **self.ArrowPaddy)
        self.LargestWordFound = ttk.Label(self._frame)
        self.LargestWordFound.grid(row=3, column=2, **self.LabPaddy)


        ttk.Button(self._frame, text="See All Monkeys", command=lambda: self.swapFrame(self.renderAllMonkeyData)).grid(row=4, column=0, columnspan=3)
        
        self.BackHomeTimeSinceStart(row=5, columnSpan=3)
    
    def renderAllMonkeyData(self):
        def monkeyInfo(row,i):
            self.monkeysOnDisplay.append([i])
            self.monkeysOnDisplay[-1].append(ttk.Label(self._frame))
            self.monkeysOnDisplay[-1].append(ttk.Label(self._frame))
            self.monkeysOnDisplay[-1].append(ttk.Label(self._frame))
            
            ttk.Label(self._frame, text=monkeys[i].name).grid(row=row, column=0)
            self.monkeysOnDisplay[-1][1].grid(row=row,column=1)
            self.monkeysOnDisplay[-1][2].grid(row=row,column=3) 
            self.monkeysOnDisplay[-1][3].grid(row=row,column=2)
            
            ttk.Button(self._frame, text="More Info", command=lambda:print(str(i), "More Info")).grid(row=row, column=4)
            ttk.Button(self._frame, text="Pause", command=lambda:print(str(i), "Pause")).grid(row=row, column=5)
            ttk.Button(self._frame, text="Delete", command=lambda:print(str(i), "Delete")).grid(row=row, column=6)

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
        if self.numMonkAlreadyLoaded < len(monkeys):
            ttk.Button(self._frame, text="More Monkeys", 
                       command=lambda:self.swapFrame(self.renderAllMonkeyData, refresh=True)
                       ).grid(row=row, column=0, columnspan=7)
            row= row +1 
        self.BackHomeTimeSinceStart(row=row, columnSpan=7, 
                                    customBackKwargs={"_dontAddToBackLog":True, "destroyerFunc":self.delRenderAllMonkeyData }, 
                                    customHomeKwargs={"destroyerFunc":self.delRenderAllMonkeyData})
    
    def delRenderAllMonkeyData(self):
        del self.numMonkAlreadyLoaded, self.monkeysOnDisplay
    
    def BackHomeTimeSinceStart(self, *, row, column=0, columnSpan=5,customHomeKwargs={}, customBackKwargs={"_dontAddToBackLog":True}): 
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
    
    
@cache
def currentwInALLW(word: str) -> bool:
    if not (2 < len(word) < 10):
        return False
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

def monkeyHandeler(numMonkeys: int, * , noPrint=False) -> None:
    global monkeys, monkeyThreads
    
    try: # Creates the variables if they are missing 
        monkeys; monkeyThreads
    except:
        monkeys, monkeyThreads = [], [] 
    
    for monkeyNum in range(numMonkeys):
        monkeys.append(monkey(f"Monkey - {monkeyNum+1}", noPrint))
        monkeyThreads.append(Thread(target=monkeys[-1].guessWord))
        monkeyThreads[-1].start()

def _pass(*args, **kwargs): pass

ALLWORDS = [word for word in ALLWORDS if len(word) > 3 and len(word) < 10]
ALLLETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
SPACEFREQUENCY = 5
for _ in range(SPACEFREQUENCY):
    ALLLETTERS.append(' ')


if __name__ == "__main__":
    NUMOFMONKEYS:int = 1
    #As type annotations cannot be declared as global inside of functions 
    monkeys: list[monkey] = []
    monkeyThreads: list[Thread] = []
    
    HowManyMonkeys().mainloop()
    Thread(monkeyHandeler(NUMOFMONKEYS)).start()
    
    MainWindowIME().mainloop()

    #TODO add a search