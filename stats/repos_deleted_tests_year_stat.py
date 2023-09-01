"""
Computes test-deletion stat across projects version
"""

import os.path
from pathlib import Path
import pandas as pd
import os
import json
import numpy as np
import sys

sys.path.append("../")
# Redirect console ouput to a file
sys.stdout = open("../stats/all_repos_deleted_test_year_stat.txt", "w")

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]



all_data_del_commits = []
all_data_del_tests = []
total_year_w_del_tests = 0

for index, project in enumerate(projects_list):
    
    def main(project):
        global all_data_del_commits, all_data_del_tests, total_year_w_del_tests
        print(project)
        print("-----------------")
        VALIDATION_FILES_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/stat_test_deletion_commits_grouped_year.csv"
        )

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")
            print("Total years w del tests", df.shape[0])
            total_year_w_del_tests += df.shape[0]
            print("Testcase")
            print("----")
            deleted_tests= list(df["Testcase"])
            all_data_del_tests = [*all_data_del_tests, *deleted_tests]
            print("Mean: ", np.mean(df["Testcase"]))
            print("Median: ", np.median(df["Testcase"]))
            print("Q1: ", np.percentile(df["Testcase"], 25))
            print("Q3: ", np.percentile(df["Testcase"], 75))
            print("Commit")
            print("----")
            deletion_commits= list(df["Commit"])
            all_data_del_commits = [*all_data_del_commits, *deletion_commits]
            print("Mean: ", np.mean(df["Commit"]))
            print("Median: ", np.median(df["Commit"]))
            print("Q1: ", np.percentile(df["Commit"], 25))
            print("Q3: ", np.percentile(df["Commit"], 75))
            
            print("xxxxx")
           
        print("================================")

    main(project)


print("--********-----")
print("All Projects")
print("Total years w del tests", total_year_w_del_tests)
print("Testcase")
print("----")
print("Mean: ", np.mean(all_data_del_tests))
print("Median: ", np.median(all_data_del_tests))
print("Q1: ", np.percentile(all_data_del_tests, 25))
print("Q3: ", np.percentile(all_data_del_tests, 75))
print("xxxxx")
print("Commit")
print("----------")
print("Mean: ", np.mean(all_data_del_commits))
print("Median: ", np.median(all_data_del_commits))
print("Q1: ", np.percentile(all_data_del_commits, 25))
print("Q3: ", np.percentile(all_data_del_commits, 75))
