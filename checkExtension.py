import sys
import os
from os import listdir
from os.path import isfile, join



def reader():
    [_,dir] = sys.argv
    extensions = {}
    readerFiles(dir, extensions)
    print(extensions)   

def readerFiles(path, extensions):
             
    for f in listdir(path):
        if isfile(join(path, f)):
            extension = f.split(".").pop()
            if not extension in extensions:
                extensions[extension] = 1
            else:
                extensions[extension] +=1
        else:
            dir = f"{path}/{f}"
            readerFiles(dir,extensions)

if __name__ == "__main__":
    reader()