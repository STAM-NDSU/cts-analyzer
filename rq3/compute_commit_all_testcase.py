import sys

sys.path.append("../")
# Redirect console ouput to a file
sys.stdout = open("../temp2_rq3.txt", "w")

import os
from typing import Optional, List
from analyzer.utils import (
    is_candidate_test_file, strip_commit_url
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
    # "cts",
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
    if not os.path.exists(
        f"{repo_path}"
    ):
        print(
            "Error: path does not exit -> ",
            repo_path,
        )
        break
    if not os.path.exists(
        f"{validated_tests_file_path}"
    ):
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
    os.chdir(repo_path) # Change directory; You are now inside the project directory
    for commit in commits_list:
        commit = strip_commit_url(commit)
        cmd = f'git checkout {commit}'
        os.system(cmd)

        print("Git checkout out: ", commit)
       
        global_testsuite_content = ""
        global_testsuite_history = {}
        line = 1
        for root, dirs, files in os.walk("./", topdown=False):
            for name in files:
                name = name.replace("$", "")
                print(name,dirs, root)
                if is_candidate_test_file(name):
                    if not os.path.exists(f"{os.path.join(root, name)}"):
                        print(
                            "Error: path does not exit -> ",
                            os.path.join(root, name),
                        )
                        break
                    with open(os.path.join(root, name), "r") as f:
                        
                        content = ''
                        try:
                            content = f.read()
                        except Exception as e:
                            content = ''
                            
                        if not content: 
                            continue
                        
                        content = content.replace("\n", "").replace("\t", "").replace("\r", "")
                        if global_testsuite_content:
                            global_testsuite_content = global_testsuite_content + "\n" + content
                        else:
                            global_testsuite_content = content
                        global_testsuite_history[os.path.join(root, name)] = line
                        line +=1

        print(all_commits_data) 
        f = open("../../cts-analyzer/io/rq3/all_commits_all_testcases/" + project + '/' + project + "-" + commit + "-ts.txt", "w")
        f.write(global_testsuite_content)
        f = open("../../cts-analyzer/io/rq3/all_commits_all_testcases/" + project + '/' + project + "-" + commit + "-tsh.json", "w")
        f.write(json.dumps(global_testsuite_history, indent=4))
    print("=========================")

    os.chdir(current_state) # Change back to original state; You are now inside root directory
sys.stdout.close()


