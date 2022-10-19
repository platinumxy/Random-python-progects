from plyer import notification


# Folowing code taken from folder and file handler see there for explaination and docs
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
    

app_icon = "image.ico"
#Used to avoid issues coming from IDEs not running code in correct folder 
MoveTo(app_icon)

notification.notify(
    title = 'Important!!!',
    message = 'This is an important notification!!\nPlease read me!!\nHave a good day <3',
    app_name = "Platinumxy's App",
    app_icon = resource_path(app_icon),
    timeout = 10,
)