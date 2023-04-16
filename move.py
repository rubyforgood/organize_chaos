import json
import sys
import subprocess
import os
import pandas as pd

[_, FINAL_OUTPUT] = sys.argv

SHORT_NAME_TO_FILE_NAME = {
    "motel": "Motel",
    "bso": "Business Support Office",
    "edo": "Equity Development Office",
    "rso": "Resident Support Office",
    "comm": "Communication",
    "admin": "Admin",
}


# Test JSON
# --------------------
# [
#   {
#     "file": "marian@outlook.com/first-file.docx",
#     "matches": {
#       "Business Support Office": 17,
#       "Motel": 23
#     }
#   },
#   {
#     "file": "marian@outlook.com/second-file.pdf",
#     "matches": {
#       "Resource Support Office": 1,
#     }
#   },
#   ...more sorted file objects
# ]

# Notes: The `cp` command will copy. To copy and remove the original file, use the
# `mv` command instead.
# --------------------
# REMEMBER: The `mv` command WILL permanently remove the original file, so use the
# `cp` command until positive this code does what you want.

data_Frame = pd.read_csv(FINAL_OUTPUT)
sorted_file_array = list(data_Frame["File"])

    # Loop on array of arrays


    
for index in range(len(sorted_file_array)):
    file = sorted_file_array[index]
    folder = list(data_Frame["Folder"])[index]
    
    # Get the file and category
    category = folder.replace("\n","")

        #  --- DEPRECATED  --------------

        # Get the matches
        # category_matches = file_dict["matches"]
        # max matches
        # max_matches = max(category_matches.values())
        # Filter all the match objects in the file's matches, in most cases we
        # should only have one thing have the most matches, but if we have multiple
        # we'll need user intervention
        # --------------
        # category: list = list(
        #     # Filter
        #     filter(
        #         # Inline function for checking if the category has the max number of matches
        #         lambda cat_key: category_matches[cat_key] == max_matches,
        #         # Pass the keys of the match dict to filter on
        #         category_matches.keys(),
        #     )
        # )

        # If the length is bigger than 1, then allow a user to look at the file name and put in a guess
        # Also let the user know how many categories have the max number of matches
        # --------------
        # if len(category) > 1:
        #     category: str = category[
        #         int(
        #             input(
        #                 f"/n/nThe file in question: `{file}`/n/nIt has multiple categories: {category}/n/nEnter the index of the category: "
        #             )
        #         )
        #     ]
        # else:
        #     category: str = category.pop()

        # Assign where the file will be copies to
    moved_dir=os.path.join("C:/Users/ramosv/Desktop/MileHighHack/organize_chaos/GoogleDrive/", category)
    #moved_dir = f"C:/Users/ramosv/Desktop/MileHighHack/organize_chaos/GoogleDrive/{category}"
    # Run the subprocess to move it.
    subprocess.run(["cp", file, moved_dir])
