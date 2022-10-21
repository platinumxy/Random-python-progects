from dataclasses import dataclass,field
from functools import cache
from time import sleep
from random import choice
from allwords import ALLWORDS
import threading
import tkinter
from typing import List

class display(tkinter.Tk):
    def __init__(self, NumMonk: int) -> None:
        tkinter.Tk.__init__(self)
        self.title('Server')
        self.configure(background='#f0f0f0')
        self.protocol('WM_DELETE_WINDOW', self.Close)
        self.monkeys = []


    def Close(self):
        self.destroy()

    def ClearPage(self): 
        for child in self.winfo_children(): child.destroy()
    
    def mainpage(self):
        self.ClearPage()

@dataclass
class monkey:
    name: str
    words: list = field(default_factory=list)

    def GuessWord(self):
        """The Monkey endlessly trys to make a word and if it does it adds it to its word set """
        while True:
            #sleep(0.00000000001)
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
                if not (word in self.words) :
                    self.words.append(word)
                    print(self.name, word)
    
    def LargestWord(self):
        """Returns the largest word that the Monkey has found """
        returnWord = ""
        for word in self.words :
            if len(word) >= len(returnWord):
                returnWord = word
        return returnWord
    
    def NumWords(self):
        """Returns the number of words the monkey has found"""
        return len(self.words)

class HowManyMonkeys(tkinter.Tk):
    """Creates a pop up box that sets numberOfMonkeys to the input"""
    def __init__(self):tkinter.Tk.__init__(self);self.title('How many monkeys?');self.geometry('300x100');self.configure(bg='#f0f0f0');self.protocol('WM_DELETE_WINDOW',lambda:self.Close());self.numOfMonkeys=tkinter.IntVar();self.numOfMonkeys.set(1);self.numOfMonkeys.trace('w',lambda name,index,mode,numOfMonkeys=self.numOfMonkeys:self.updateMonkeys());tkinter.Label(self,text='How many monkeys?').grid(row=0,column=0,columnspan=2);tkinter.Entry(self,textvariable=self.numOfMonkeys).grid(row=1,column=0);self.monkeys=[];self.startButton=tkinter.Button(self,text='Start',command=lambda:self.start());self.startButton.grid(row=2,column=0,columnspan=2);self.updateMonkeys()
    def updateMonkeys(self):self.startButton.config(text='Start ('+str(self.numOfMonkeys.get())+')')
    def start(self):global numberOfMonkeys;numberOfMonkeys=self.numOfMonkeys.get();self.destroy()


@cache
def realWord(word):
    """Returns if a word is a real word"""
    return (word in ALLWORDS)

ALLWORDS = [word for word in ALLWORDS if len(word) > 2] # removes the one letter and two letter words from the Words list
chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
for i in range(3): # incresse the value to incresse the probibility of the monkey choing a space
    chars.append(" ")

numberOfMonkeys = 0
HowManyMonkeys().mainloop()

