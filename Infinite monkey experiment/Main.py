from dataclasses import dataclass, field
from functools import cache
from time import sleep
from random import choice
from allwords import ALLWORDS
import threading
import tkinter as TK 
from typing import List


class HowManyMonkeys(TK.Tk):
    """Creates a pop up box that sets numberOfMonkeys to the input"""
    def __init__(self): TK.Tk.__init__(self); self.title('How many monkeys?'); self.geometry('300x100'); self.configure(bg='#f0f0f0'); self.protocol('WM_DELETE_WINDOW', lambda: self.Close()); self.numOfMonkeys=TK.IntVar(); self.numOfMonkeys.set(1); self.numOfMonkeys.trace('w', lambda name, index, mode, numOfMonkeys=self.numOfMonkeys: self.updateMonkeys()); TK.Label(self, text='How many monkeys?').grid(row=0, column=0, columnspan=2); TK.Entry(self, textvariable=self.numOfMonkeys).grid(row=1, column=0); self.monkeys=[]; self.startButton=TK.Button(self, text='Start', command=lambda: self.start()); self.startButton.grid(row=2, column=0, columnspan=2); self.updateMonkeys()
    def updateMonkeys(self): self.startButton.config(text='Start ('+str(self.numOfMonkeys.get())+')')
    def start(self): global numberOfMonkeys; numberOfMonkeys = self.numOfMonkeys.get(); self.destroy()
    def close(self):
        from os import _exit
        self.destroy();_exit(0)

@dataclass
class monkey:
    name: str
    words: list = field(default_factory=list)

    def GuessWord(self):
        """The Monkey endlessly trys to make a word and if it does it adds it to its word set """
        while True:
            # sleep(0.00000000001)
            sleep(0)
            word = []
            letter: str
            while True:
                letter = choice(chars)
                if letter == " ":
                    break
                word.append(letter)

            word = "".join(word)
            if realWord(word):
                if not (word in self.words):
                    self.words.append(word)
                    print(self.name, word)

    def LargestWord(self):
        """Returns the largest word that the Monkey has found """
        returnWord = ""
        for word in self.words:
            if len(word) >= len(returnWord):
                returnWord = word
        return returnWord

    def NumWords(self):
        """Returns the number of words the monkey has found"""
        return len(self.words)


class display(TK.Tk):
    def __init__(self) -> None:
        TK.Tk.__init__(self)
        self.title('Infinite monkey experiment')
        self.configure(background='#f0f0f0')
        self.protocol('WM_DELETE_WINDOW', self.Close)
        #creates the updater that will update all of the text vars 
        self.updater = threading.Thread(target=self.updatePages)
        self.mainpage()

    def Close(self):
        self.destroy()

    def ClearPage(self):
        for child in self.winfo_children():
            child.destroy()

    def mainpage(self):
        self.ClearPage()
        self.activePage = self.mainpage
        TK.Label(self, text="The Endless monkeys").grid(row=0,column=0,columnspan=1)
        self.largestword = TK.StringVar(value=largestWord())
        self.numWords = TK.StringVar(value=str(howmanywords()))

        TK.Label(self, text="Largest Word").grid(row=1,column=0)
        TK.Label(self, textvariable=self.largestword).grid(row=1,column=1)

        TK.Label(self, text="Number of Words").grid(row=2,column=0)
        TK.Label(self, textvariable=self.numWords).grid(row=2,column=1)
    
        

    def updatePages(self):
        sleep(1)
        if self.activePage == self.mainpage :
            self.largestword.set(largestWord())
            self.numWords.set(str(howmanywords())) 
 
@cache
def realWord(word):
    """Returns if a word is a real word"""
    return (word in ALLWORDS)

def howmanywords():
    global monkeys 
    wordCount = 0
    for Monk in monkeys :
        wordCount = wordCount + Monk.NumWords()
    return wordCount

def largestWord():
    global monkeys
    largestWord = ""
    for Monk in monkeys :
        monkWord = Monk.LargestWord()
        if len(largestWord) < len(monkWord) :
            largestWord = monkWord 

def pageHolder():
    global page
    page = display()
    page.mainloop()

def autoRefresher(func):
    while True :
        sleep(0.1)
        func()

# removes the one letter and two letter words from the Words list
ALLWORDS = [word for word in ALLWORDS if len(word) > 2]
chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
         "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
monkeys = []
for i in range(3):  # incresse the value to incresse the probibility of the monkey choing a space
    chars.append(" ")

#Gets the number of monkeys that the user wants 
numberOfMonkeys = 0
HowManyMonkeys().mainloop()


def monkeyHandeler():
    global monkeys 
    for i in range(numberOfMonkeys):
        monkeys.append(monkey(f"Monkey {i+1}"))
    monkeyThreads = [threading.Thread(target=Monk.GuessWord) for Monk in monkeys]
    for thread in monkeyThreads :
        thread.start()
    monkeyThreads[0].join()


App = display()
#Use page holder as display is a child of TK and it wants to be called from the the same thread 
#threading.Thread(target=pageHolder).start()
#Starts the pages updat


apploop = threading.Thread(target=App.mainloop)
autoRefresh = threading.Thread(target=autoRefresher, args=(App.updatePages,))
MonkHand = threading.Thread(target=monkeyHandeler)
MonkHand.start()
apploop.start()
autoRefresh.start()