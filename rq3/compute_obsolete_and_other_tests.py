"""
Compiles all phased and concurrent obsolete tests present in test deletion commit. Rest of the deleted tests are categorized as `not obsolete`.
"""

import sys

sys.path.append("../")
# Redirect console ouput to a file
# sys.stdout = open("../temp_rq3.txt", "w")

import os
from analyzer.utils import (
    strip_commit_url,
)
import json
from pathlib import Path
import pandas as pd


PROJECT_DIR = "../../os-java-projects/"
projects_list = [
    # "commons-lang",
    # "gson",
    # "commons-math",
    # "jfreechart",
    # "joda-time",
    "pmd",
]
VALIDATION_DIR = "../io/validationFiles"


# Get all functions present in the parent commit as list
# INFO: Return False if parent commit function history file does not exist
def get_all_functions_parent_commit(project, commit):
    dirpath = "../io/rq3/all_commits_all_functions/" + project
    filename = project + "-" + commit + ".json"
    full_path = dirpath + "/" + filename
    if not os.path.exists(full_path):
        print(
            "Error: path does not exit -> ",
            full_path,
        )
        return False

    try:
        function_history = json.load(open(full_path))  # {filepath: [functions], }
        all_functions = function_history.values()
        return all_functions
    except Exception as e: 
        print("Error reading file" + full_path)
        return False
    
    


for project in projects_list:
    print("Project: ", project)

    deleted_tests_file_path = Path(f"{VALIDATION_DIR}/{project}/hydrated_rq_2.csv")
    if not os.path.exists(f"{deleted_tests_file_path}"):
        print(
            "Error: path does not exit -> ",
            deleted_tests_file_path,
        )
        break

    df = pd.read_csv(deleted_tests_file_path)
    # We set deleted test type to be `not obsolete` by default
    # We then check if it is phased obsolete or concurrent obsolete
    df["Type"] = "not obsolete"
    # Track missing invoked(referenced) functions for phased obsolete test
    df["Type Details"] = "na"

    # Modify referenced functions `NaN`` values of each deleted test to empty string
    # INFO: They are not obsolete tests
    df["Referenced Functions"] = df['Referenced Functions'].fillna('')
    
    for index, row in df.iterrows():
        # Check if the deleted test is concurent obsolete
        if row["Deleted With Source Code"] == "yes":
            df.loc[index, "Type"] = "concurrent obsolete"
        else:
            parent_commit = row["Parent"]
            parent_commit_sha = strip_commit_url(parent_commit)
            parent_all_functions = []
            result = get_all_functions_parent_commit(project, parent_commit_sha)

            # Check if parent function history file existed i.e return value in not Boolean `False`
            if result != False:
                parent_all_functions = result
            else:
                break

            # For each deleted testcase get all invoked functions in the body
            invoked_functions = str(row["Referenced Functions"]).split(",")
            invoked_functions = list(filter(None, invoked_functions)) # Remove empty strings
            
            # Skip if there are no referenced functions
            # if(not invoked_functions):
            #     break
            
            # Check if the deleted test is phased obsolete
            for func in invoked_functions:
                # Check if invoked function is not present in the parent commit functions
                if func not in parent_all_functions:
                    df.loc[index, "Type"] = "phased obsolete"
                    df.loc[index, "Type Details"] = func
                    break

    full_output_file_path = Path(
        f"{VALIDATION_DIR}/{project}/hydrated_rq_2_with_deletion_type.csv"
    )
    df.to_csv(f"{full_output_file_path}", index=False)
    print(f"Generated {full_output_file_path}")

# sys.stdout.close()
