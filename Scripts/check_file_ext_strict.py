import sys
from os import listdir
from os.path import isdir, isfile, join
import json
import pandas as pd


def read_json() -> dict:
    with open("./Resources/lexicon.json", "r") as j:
        lex = json.loads(j.read())
    return lex


def count_file_ext():
    [_, dir] = sys.argv
    extensions = {}
    check_file_ext(dir, extensions)


def check_file_ext(path, extensions):
    for f in listdir(path):
        if isfile(join(path, f)):
            extension = f.split(".").pop()
            if not extension in extensions:
                extensions[extension] = 1
            else:
                extensions[extension] += 1
        else:
            dir = f"{path}/{f}"
            check_file_ext(dir, extensions)


def checkForLex(path):
    lex = read_json()
    main_list = []
    for file in listdir(path):
        for word in lex:
            if isdir(file) and word.lower() in file.lower():
                main_list.append([file, word])
            else:
                continue

    df = pd.DataFrame(main_list, columns=["File name", "Word"])
    return df


if __name__ == "__main__":
    path = "C:/Users/ramosv/Desktop/MileHack - The Fax Denver"
    checkForLex(path)
