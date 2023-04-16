from tdqm import tqdm
from os.path import join, isfile, isdir

import os
import json
import sys

[_, DOCUMENTS] = sys.argv
MISC_FILE_EXT = [
    "xlsx",
    "html",
    # "pdf",
    "png",
    # "docx",
    "jpg",
    "jpeg",
    "zip",
    "pptx",
    "xls",
    "pages",
    # "csv",
    "m4a",
    # MAYBE GET TXT
    "txt",
    "conf",
    "mp4",
    "doc",
]


def run_analysis():
    local_path = DOCUMENTS
    os.chdir(local_path)
    files = [
        os.path.join(dir_path, f)
        for dir_path, dir_names, filenames in os.walk(os.getcwd())
        for f in filenames
    ]

    matched_files_level_1 = []
    unmatched_files_level_1 = []

    # Filter by file name
    for file in tqdm(files):
        classify_on_file_name(file, matched_files_level_1, unmatched_files_level_1)

    matched_files_level_2 = []
    unmatched_files_level_2 = []
    # Filter by extension
    for file in tqdm(unmatched_files_level_1):
        classify_on_ext(files, matched_files_level_2, unmatched_files_level_2)

    matched_files_level_3 = classify_on_model(unmatched_files_level_2)

    all_matched_files = (
        matched_files_level_1 + matched_files_level_2 + matched_files_level_3
    )

    print(all_matched_files)


if "__main__" == __name__:
    run_analysis()


def classify_on_file_name(file, unmatched, matched):
    lexicon_dict: dict = readDir()

    # Boolean to tell us whether we found a match
    found_match = False
    # Assign a dictionary to the file we are sorting
    sorted_file_dict = {"file": file}

    # For every category...
    for category in lexicon_dict.keys():
        # For every keyword in out lexicon array for the category...
        for keyword in lexicon_dict[category]:
            # If the keyword is in the file name, we have a match
            if keyword.lower() in file.lower():
                found_match = True
                # If the category key isn't in the matches, then assign it
                if category not in sorted_file_dict["matches"]:
                    sorted_file_dict["folder"] = category
            # If no match, don't do shit
            else:
                continue

    if found_match:
        matched.append(sorted_file_dict)
    else:
        unmatched.append(file)


def classify_on_ext(file, unmatched, matched):
    extension = file.split(".").pop()
    if extension in MISC_FILE_EXT:
        matched


def classify_on_model():
    pass


def readDir():
    with open("./Resources/lexicon.json", "r") as j:
        lex = json.loads(j.read())
    return lex
