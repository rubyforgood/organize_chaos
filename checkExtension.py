import sys
import os
from os import listdir
from os.path import isfile, join
import json
import pandas as pd


def readDir():
    with open('./Resources/lexicon.json', 'r') as j:
        lex = json.loads(j.read())
    return lex
    

def reader():
    [] = sys.argv
    #[_,dir] = sys.argv
    #extensions = {}
    #readerFiles(dir, extensions)
    #print(extensions)   

# def readerFiles(path, extensions):
             
#     for f in listdir(path):
#         if isfile(join(path, f)):
#             extension = f.split(".").pop()
#             if not extension in extensions:
#                 extensions[extension] = 1
#             else:
#                 extensions[extension] +=1
#         else:
#             dir = f"{path}/{f}"
#             readerFiles(dir,extensions)

def checkForLex(path):
    lex = readDir()
    mainList = []
    for f in listdir(path):
        for word in lex:
            if word.lower() in f.lower():
                mainList.append([f,word])
            else:
                continue
    df = pd.DataFrame(mainList, columns=["File name", "Word"])
    breakpoint()
    return df
                

if __name__ == "__main__":
    #reader()
    path = "C:/Users/ramosv/Desktop/MileHack - The Fax Denver"
    checkForLex(path)