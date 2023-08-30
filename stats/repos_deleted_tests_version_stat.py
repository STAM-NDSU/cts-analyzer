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
sys.stdout = open("../stats/all_repos_deleted_test_version_stat.txt", "w")

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

for index, project in enumerate(projects_list):
    
    def main(project):
        global all_data_del_commits, all_data_del_tests
        print(project)
        print("-----------------")
        VALIDATION_FILES_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/stat_version_test_deletion.csv"
        )

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")
            df = df[df['Test Deletion Commits'] > 0]
            print("Total Deleted Tests")
            print("----")
            deleted_tests= list(df["Total Deleted Tests"])
            all_data_del_tests = [*all_data_del_tests, *deleted_tests]
            print("Mean: ", np.mean(df["Total Deleted Tests"]))
            print("Median: ", np.median(df["Total Deleted Tests"]))
            print("Q1: ", np.percentile(df["Total Deleted Tests"], 25))
            print("Q3: ", np.percentile(df["Total Deleted Tests"], 75))
            
            print("xxxxx")
            print("Test deletion commits")
            print("----")
            deletion_commits= list(df["Test Deletion Commits"])
            all_data_del_commits = [*all_data_del_commits, *deletion_commits]
            print("Mean: ", np.mean(df["Test Deletion Commits"]))
            print("Median: ", np.median(df["Test Deletion Commits"]))
            print("Q1: ", np.percentile(df["Test Deletion Commits"], 25))
            print("Q3: ", np.percentile(df["Test Deletion Commits"], 75))
        print("================================")

    main(project)


print("--********-----")
print("All Projects")
print("xxxxx")
print("Total Deleted Tests")
print("----")
print("Mean: ", np.mean(all_data_del_tests))
print("Median: ", np.median(all_data_del_tests))
print("Q1: ", np.percentile(all_data_del_tests, 25))
print("Q3: ", np.percentile(all_data_del_tests, 75))
print("xxxxx")
print("Total Deletion Commits")
print("-----")
print("Mean: ", np.mean(all_data_del_commits))
print("Median: ", np.median(all_data_del_commits))
print("Q1: ", np.percentile(all_data_del_commits, 25))
print("Q3: ", np.percentile(all_data_del_commits, 75))
print("xxxxx")