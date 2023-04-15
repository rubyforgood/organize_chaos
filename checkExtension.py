import sys
import os
from os import listdir
from os.path import isfile, join
import json
import pandas


def readDir():
    with open('./Resources/lexicon.json', 'r') as j:
        lex = json.loads(j.read())
    return list(lex.keys())
    

def reader():
    [] = sys.argv
    #[_,dir] = sys.argv
    #extensions = {}
    #readerFiles(dir, extensions)
    #print(extensions)   

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

def checkForLex(path):
    lex = readDir()
    mainList = []
    for f in listdir(path):
        for word in lex:
            if word in lex:
                mainList.append(())
                
    

if __name__ == "__main__":
    #reader()
    path = "C:/Users/ramosv/Desktop/MileHack - The Fax Denver"
    checkForLex(path)