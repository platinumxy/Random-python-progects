import os, sys 
def getDataFromFolder(folder,*, BitFiles=False):
    data = ""
    bitData = b''
    for file in os.listdir(folder):
        if os.path.isdir(file):
            data = data + getDataFromFolder(folder + file)
        else: 
            try : 
                with open(folder+"\\"+file, "r") as openFile : 
                    data = data + (openFile.read()).replace("\n","")
            except UnicodeDecodeError:
                if BitFiles:
                    with open(folder+"\\"+file, "rb") as openFile:
                        bitData = bitData + openFile.read()
            except PermissionError :
                pass
    return data + str(bitData)

if __name__ == "__main__":
    print(getDataFromFolder(input("Enter Folder Path\n")))

