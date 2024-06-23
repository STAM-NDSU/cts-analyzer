"""
Compiles all phased obsolete tests present in test deletion commit
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
    "gson",
    # "commons-math",
    # "jfreechart",
    # "joda-time",
    # "pmd",
    # "cts",
]
VALIDATION_DIR = "../io/validationFiles"
current_state = os.getcwd()

for project in projects_list:
    print("Project: ", project)
    
    deleted_tests_file_path = Path(
        f"{VALIDATION_DIR}/{project}/hydrated_rq_2.csv"
    )
    if not os.path.exists(f"{deleted_tests_file_path}"):
        print(
            "Error: path does not exit -> ",
            deleted_tests_file_path,
        )
        break

    df = pd.read_csv(deleted_tests_file_path)
    
    # Get all functions present in the parent commit
    def get_all_functions_parent_commit(project, commit):
        dirpath = "../../cts-analyzer/io/rq3/all_commits_all_functions/"+ project
        filename = project + "-"  + commit+ ".json"
        full_path = dirpath + "/" + filename
        if not os.path.exists(full_path):
            print(
                "Error: path does not exit -> ",
                full_path,
            )
            break
        
        function_history = json.load(open(full_path)) # {filepath: [functions], }
        all_functions = function_history.dict.values()
        print(all_functions)
        
    
    for index, row in df.iterrows():
        
        # Check if the deleted test is concurent obsolete
        if row["Delete with Source Code"] == "yes":
            row["Type"] = "Concurrent Obsolete"
        else:
            parent_commit = row["Parent"]
            parent_commit_sha = strip_commit_url(parent_commit)
            parent_all_functions = get_all_functions_parent_commit(project, parent_commit_sha)
            
            invoked_functions = row["Referenced Functions"]
            type = "redundant"
            for func in invoked_functions:
                if func not in parent_all_functions:
                    type = "Phased Obsolete"
                    break
                
            row["Type"] = type
    
    full_output_file_path = Path(
        f"{VALIDATION_DIR}/{project}/hydrated_rq_2_with_deletion_type.csv"
    )
    df.to_csv(f"{full_output_file_path}", index=False)
    print(f"Generated {full_output_file_path}")
    
    # For each row
    # Get deleted testcase
    # For each deleted testcase get all invoked functions
    
    #### check if invoked function is present in the parent commit functions list; if any function is absent it is 
    #### phased obsolete test
    

# sys.stdout.close()


