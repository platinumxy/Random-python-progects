def timeFunction(function):
    from time import time 
    def __Timer(*args, **kwargs) :
        startTime = time()
        function(*args, **kwargs)
        print(f"{function.__name__} took - {time() - startTime} seconds") 
    return __Timer