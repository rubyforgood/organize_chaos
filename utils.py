import json
import subprocess


# The JSON needs to be structured in this way, an array of dictionaries that has
# a "file" key and a "category" key
# --------------------
# [
#     {
#         "file": "checkExtension.py",
#         "category": "Test",
#     }
# ]

# Notes: The `cp` command will copy. To copy and remove the original file, use the
# `mv` command instead.
# --------------------
# REMEMBER: The `mv` command WILL permanently remove the original file, so use the
# `cp` command until positive this code does what you want.


# This code can also move to the file that would right the JSON and then
# we can just call the for loop on the array of sorted files
_ = "path-to-file"

with open(_, "r") as sorted_file_json:
    # Load JSON and get array of dictionaries
    sorted_file_dicts = json.loads(sorted_file_json.read())
    # Loop on array of dictionaries
    for file_dict in sorted_file_dicts:
        # Get the file and category
        file = file_dict["file"]
        category = file_dict["category"]

        # Assign where the file will be copies to
        moved_dir = f"./Categories/{category}"
        # Run the subprocess to move it.
        subprocess.run(["cp", file, moved_dir])
