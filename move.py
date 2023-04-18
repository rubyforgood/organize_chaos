import os
import pandas as pd
import sys
import subprocess

[_, FINAL_OUTPUT] = sys.argv

SHORT_NAME_TO_FOLDER_NAME = {
    "motel": "Motel",
    "bso": "Business Support Office",
    "edo": "Equity Development Office",
    "rso": "Resident Support Office",
    "comm": "Communication",
    "admin": "Admin",
}

# Notes: The `cp` command will copy. To copy and remove the original file, use the
# `mv` command instead.
# --------------------
# REMEMBER: The `mv` command WILL permanently remove the original file, so use the
# `cp` command until positive this code does what you want.
if "__main__" == __name__:
    data_frame = pd.read_csv(FINAL_OUTPUT)
    sorted_file_array = list(data_frame["File"])
    sorted_folder_array = list(data_frame["Folder"])

    if len(sorted_file_array) != len(sorted_folder_array):
        raise Exception(
            "\nCannot load in file-folder CSV if there are some files without folders."
        )

    # Loop on array of arrays
    for index in range(len(sorted_file_array)):
        # Get the file based on index
        file = sorted_file_array[index]
        # Get the folder based on index
        folder = sorted_folder_array[index]

        # Get the file and category
        category = folder.replace("\n", "")

        # Assign where the file will be copies to
        moved_dir = os.path.join(
            "C:/Users/ramosv/Desktop/MileHighHack/organize_chaos/GoogleDrive/", category
        )
        # Run the subprocess to move it.
        subprocess.run(["cp", file, moved_dir])
