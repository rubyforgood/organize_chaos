import json
import subprocess


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


# This code can also move to the file that would right the JSON and then
# we can just call the for loop on the array of sorted files
_ = "./test.json"

with open(_, "r") as sorted_file_json:
    # Load JSON and get array of dictionaries
    sorted_file_dicts = json.loads(sorted_file_json.read())
    # Loop on array of dictionaries
    for file_dict in sorted_file_dicts:
        # Get the file and category
        file = file_dict["file"]
        # Get the matches
        category_matches = file_dict["matches"]
        # max matches
        max_matches = max(category_matches.values())
        # Filter all the match objects in the file's matches, in most cases we
        # should only have one thing have the most matches, but if we have multiple
        # we'll need user intervention
        category: list = list(
            # Filter
            filter(
                # Inline function for checking if the category has the max number of matches
                lambda cat_key: category_matches[cat_key] == max_matches,
                # Pass the keys of the match dict to filter on
                category_matches.keys(),
            )
        )

        # If the length is bigger than 1, then allow a user to look at the file name and put in a guess
        # Also let the user know how many categories have the max number of matches
        if len(category) > 1:
            category: str = category[
                int(
                    input(
                        f"\n\nThe file in question: `{file}`\n\nIt has multiple categories: {category}\n\nEnter the index of the category: "
                    )
                )
            ]
        else:
            category: str = category.pop()

        # Assign where the file will be copies to
        moved_dir = f"./Testing/{category}"
        # Run the subprocess to move it.
        subprocess.run(["cp", file, moved_dir])
