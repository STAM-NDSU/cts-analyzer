"""
Compiles all functions present in the parent commits of test deletion commit in a single function history file
"""
import sys

sys.path.append("../")
# Redirect console ouput to a file
# sys.stdout = open("../temp_rq3.txt", "w")

import os
from typing import Optional, List
from analyzer.utils import (
    is_candidate_test_file,
    strip_commit_url,
    is_candidate_java_file,
    get_function_name_from_prototype_lizard,
    get_function_name_from_prototype,
)
from analyzer.pattern import Pattern
import re
import glob
import json
from pathlib import Path
import pandas as pd
import lizard

PROJECT_DIR = "../../os-java-projects/"
projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
]
VALIDATION_DIR = "../io/validationFiles"
current_state = os.getcwd()

for project in projects_list:
    print("Project: ", project)
    repo_path = PROJECT_DIR + project
    print(repo_path)
    validated_tests_file_path = Path(
        f"{VALIDATION_DIR}/{project}/validation_diff_done_hydrated.csv"
    )
    if not os.path.exists(f"{repo_path}"):
        print(
            "Error: path does not exit -> ",
            repo_path,
        )
        break
    if not os.path.exists(f"{validated_tests_file_path}"):
        print(
            "Error: path does not exit -> ",
            validated_tests_file_path,
        )
        break

    df = pd.read_csv(validated_tests_file_path)
    deleted_tc_df = df[df["Final Results"] == "yes"]
    commits_list = list(set(list(deleted_tc_df["Parent"])))
    print("Commits to scan:", len(commits_list))

    all_commits_data = {}
    os.chdir(repo_path)  # Change directory; You are now inside the project directory
    for commit in commits_list:
        commit = strip_commit_url(commit)
        
        dirpath = "../../cts-analyzer/io/rq3/all_commits_all_functions/"+ project
        filename = project + "-"  + commit+ ".json"
            
        if(os.path.exists(dirpath)== False):
            os.mkdir(dirpath)
        
        # Ignore if there is file already
        if(os.path.exists(dirpath + "/" + filename) and os.path.isfile(dirpath + "/" + filename)):
            print("Skip for " + commit + " project " + project)
            continue;  
            
        cmd = f"git checkout {commit}"
        os.system(cmd)

        print("Git checkout out: ", commit)

        all_functions_in_commits = {}
        for root, dirs, files in os.walk("./", topdown=False):
            for name in files:
                name = name.replace("$", "")
                print(name, dirs, root)
                if ".java" in name and not is_candidate_test_file(name):
                    if not os.path.exists(f"{os.path.join(root, name)}"):
                        print(
                            "Error: path does not exit -> ",
                            os.path.join(root, name),
                        )
                        break
                    else:
                        i = lizard.analyze_file(os.path.join(root, name))
                        functions_list = i.function_list
                        functions_name_list = map(
                            lambda each: get_function_name_from_prototype(
                                get_function_name_from_prototype_lizard(
                                    each.__dict__["long_name"]
                                )
                            ),
                            functions_list,
                        )
                        functions_name_list = list(set(list(functions_name_list)))
                        all_functions_in_commits[
                            os.path.join(root, name)
                        ] = functions_name_list

        all_commits_data[commit] = all_functions_in_commits
        print(all_commits_data)
        
        dirpath = "../../cts-analyzer/io/rq3/all_commits_all_functions/"+ project
        filename = project + "-"  + commit+ ".json"
            
        if(os.path.exists(dirpath)== False):
            os.mkdir(dirpath)
        
        f = open(dirpath + "/" + filename, "w")
        f.write(json.dumps(all_commits_data, indent=4))
    print("=========================")

    os.chdir(
        current_state
    )  # Change back to original state; You are now inside root directory
sys.stdout.close()
