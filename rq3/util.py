import sys

sys.path.append("../")
# Redirect console ouput to a file
# sys.stdout = open("../stats/all_repos_testcases_stat.txt", "w")

import os
from typing import Optional, List
from analyzer.utils import (
    is_candidate_test_file,
)
from analyzer.pattern import Pattern
import re
import glob
import json

target_dir = "../io/projects/"
projects_list = [
    # "commons-lang",
    "gson",
    # "commons-math",
    # "jfreechart",
    # "joda-time",
    # "pmd",
    # "cts",
]
output_dir = './'
for project in projects_list:
    print("Project: ", project)
    repo_path = target_dir + project
    print(repo_path)

    global_testsuite_content = ""
    global_testsuite_history = {}
    line = 1
    for root, dirs, files in os.walk(repo_path, topdown=False):
        for name in files:
            if is_candidate_test_file(name):
                with open(os.path.join(root, name), "r") as f:
                    content = f.read()
                    content = content.replace("\n", "").replace("\t", "").replace("\r", "")
                    if global_testsuite_content:
                        global_testsuite_content = global_testsuite_content + "\n" + content
                    else:
                        global_testsuite_content = content
                    global_testsuite_history[name] = line
                    line +=1
                    
    f = open(output_dir + project + '/' + "all_testsuite.txt", "w")
    f.write(global_testsuite_content)
    f.close()
    f = open(output_dir + project + '/' + "all_testsuite_history.txt", "w")
    f.write(json.dumps(global_testsuite_history, indent=4))
    print("=========================")

sys.stdout.close()
