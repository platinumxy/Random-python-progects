#Use this to avoid program having issues finding the icon when compiled 
def resource_path(relative_path):
    from os import path 
    try:
        from sys import _MEIPASS
        base_path = _MEIPASS
    except ImportError or Exception:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)

def MoveTo(fileName:str) ->  str:
    """finds the specified file and moves the curent working directory and returns the old directory 
    otherwise rases FileNotFoundError and returns to the original working dir  
    """
    return __RecursiveMoveTo(fileName, True)

def __RecursiveMoveTo(fileName, __START=False):
    from os import getcwd, listdir, chdir, path 
    cwd = getcwd()
    for file in listdir(cwd):
        if path.isfile(file):
            if file == fileName:
                return cwd
        else :
            try :
                chdir(cwd+"\\"+file)
                found = __RecursiveMoveTo(fileName)
                if found : 
                    return cwd 
            except NotADirectoryError:
                pass 
    if __START :
        raise FileNotFoundError()
    else:
        return False 

"""
Compressed : 


def resource_path(relative_path):
    from os import path 
    try:from sys import _MEIPASS;base_path = _MEIPASS
    except ImportError or Exception: base_path = path.abspath(".")
    return path.join(base_path, relative_path)
def MoveTo(fileName:str) ->  str: return __RecursiveMoveTo(fileName, True)
def __RecursiveMoveTo(fileName, __START=False):
    from os import getcwd, listdir, chdir, path 
    cwd = getcwd()
    for file in listdir(cwd):
        if path.isfile(file): 
            if file == fileName:return cwd
        else :
            try :
                chdir(cwd+"\\"+file)
                found = __RecursiveMoveTo(fileName)
                if found : return cwd 
            except NotADirectoryError: pass 
    if __START :raise FileNotFoundError()
    else: return False 
    
"""