class timeFunction:
    def __init__(self, function):
        from time import time
        self.func = function
        self.time = time

    def __call__(self, *args, **kwargs):
        startTime = self.time()
        self.func(*args, **kwargs)
        print(f"{self.func.__name__} took - {self.time()-startTime}")
