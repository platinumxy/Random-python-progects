import tkinter.messagebox as mb
import tkinter as tk
import tkinter.ttk as ttk
from time import time
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

    def addWordToWords(self, word) -> None:
        if not self.noPrint:
            print(self.name, "found", word)
        self.words.append(word)
        self.numWords = self.numWords + 1
        if len(word) >= len(self.largestWord):
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
        

@cache
def currentwInALLW(word: str) -> bool:
    if not (2 < len(word) < 10):
        return False
    return word[:-1] in ALLWORDS


def monkeyHandeler(numMonkeys: int, * , noPrint=False) -> None:
    monkeys: list[monkey] = []
    monkeyThreads: list[Thread] = []
    for monkeyNum in range(numMonkeys):
        monkeys.append(monkey(f"Monkey - {monkeyNum+1}", noPrint))
        monkeyThreads.append(Thread(target=monkeys[-1].guessWord))
        monkeyThreads[-1].start()


ALLWORDS = [word for word in ALLWORDS if len(word) > 3 and len(word) < 10]
ALLLETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
SPACEFREQUENCY = 5
for _ in range(SPACEFREQUENCY):
    ALLLETTERS.append(' ')



if __name__ == "__main__":
    NUMOFMONKEYS:int = 1
    HowManyMonkeys().mainloop()

    monkeyHandeler(NUMOFMONKEYS)
