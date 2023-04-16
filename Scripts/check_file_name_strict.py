from os import listdir
from os.path import isfile, join
import json


def readDir():
    with open("./Resources/lexicon.json", "r") as j:
        lex = json.loads(j.read())
    return lex


def checkForLex(path, sorted_file_dict_arr):
    lexicon_dict: dict = readDir()

    # For every thing in our directory
    for thing_in_path in listdir(path):
        # If our current iteration is a file then sort it
        if isfile(join(path, thing_in_path)):
            # Assign the file so we know it's a file
            file = thing_in_path
            # Boolean to tell us whether we found a match
            found_match = False
            # Assign a dictionary to the file we are sorting
            sorted_file_dict = {"file": file, "matches": {}}

            # For every category...
            for category in lexicon_dict.keys():
                # For every keyword in out lexicon array for the category...
                for keyword in lexicon_dict[category]:
                    # If the keyword is in the file name, we have a match
                    if keyword.lower() in file.lower():
                        found_match = True
                        # If the category key isn't in the matches, then assign it
                        if category not in sorted_file_dict["matches"]:
                            sorted_file_dict["matches"][category] = 1
                        else:
                            sorted_file_dict["matches"][category] += 1
                    # If no match, don't do shit
                    else:
                        continue

            found_match and sorted_file_dict_arr.append(sorted_file_dict)

        # If we're not a file, we are a directory, so recurse
        else:
            dir = thing_in_path
            checkForLex(join(path, dir), sorted_file_dict_arr)


if __name__ == "__main__":
    path = "C:/Users/ramosv/Desktop/MileHack - The Fax Denver"
    sorted_file_dict_arr = []
    checkForLex(path, sorted_file_dict_arr)
    # Print out our JSON
    print(sorted_file_dict_arr)
