"""
Computes days and other commits between test deletion commits stat across projects version
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
sys.stdout = open("../stats/all_repos_days_commits_inbetween_stat.txt", "w")

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]



all_data_commits_inbetween = []
all_data_days_inbetween = []

for index, project in enumerate(projects_list):
    
    def main(project):
        global all_data_commits_inbetween, all_data_days_inbetween
        print(project)
        print("-----------------")
        VALIDATION_FILES_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/test_deletion_datetime_inbetweencommits_range.csv"
        )

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")
            df= df.loc[1:, :]
            commits_inbetween= list(df["Commits"])
            all_data_commits_inbetween = [*all_data_commits_inbetween, *commits_inbetween]
            print("Commits")
            print("----")
            print("Mean: ", np.mean(df["Commits"]))
            print("Median: ", np.median(df["Commits"]))
            print("Q1: ", np.percentile(df["Commits"], 25))
            print("Q3: ", np.percentile(df["Commits"], 75))
            
            print("xxxxx")
            print("Days")
            print("----")
            days_inbetween= list(df["Range"])
            all_data_days_inbetween = [*all_data_days_inbetween, *days_inbetween]
            print("Mean: ", np.mean(df["Range"]))
            print("Median: ", np.median(df["Range"]))
            print("Q1: ", np.percentile(df["Range"], 25))
            print("Q3: ", np.percentile(df["Range"], 75))
        print("================================")

    main(project)


print("--********-----")
print("All Projects")
print("Commits")
print("----------")
print("Mean: ", np.mean(all_data_commits_inbetween))
print("Median: ", np.median(all_data_commits_inbetween))
print("Q1: ", np.percentile(all_data_commits_inbetween, 25))
print("Q3: ", np.percentile(all_data_commits_inbetween, 75))
print("xxxxx")
print("Days")
print("----")
print("Mean: ", np.mean(all_data_days_inbetween))
print("Median: ", np.median(all_data_days_inbetween))
print("Q1: ", np.percentile(all_data_days_inbetween, 25))
print("Q3: ", np.percentile(all_data_days_inbetween, 75))