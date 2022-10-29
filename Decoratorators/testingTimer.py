from time import sleep
from timer import timeFunction


@timeFunction
def mySleep(secs):
    sleep(secs)


@timeFunction
def hmm(loopcount=0):
    loopcount = loopcount + 1
    if loopcount < 100:
        return hmm(loopcount)


mySleep(2)
hmm()


def callingTimeFunction():
    # calles the __init__ method
    timeFunction()
