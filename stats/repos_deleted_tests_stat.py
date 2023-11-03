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
sys.stdout = open("../stats/all_repos_deleted_test_stat1.txt", "w")

projects_list = [
    # "commons-lang",
    "gson",
    # "commons-math",
    # "jfreechart",
    # "joda-time",
    # "pmd",
    # "cts",
]

total_commits = [
    7080,
    1771,
    7116,
    4219,
    2252,
    25422,
    401732,
]  # As per projects_list index order


all_data_del_test_per_commit = []
all_del_tests = []
total_del_commits = 0
for index, project in enumerate(projects_list):

    def main(project):
        global all_data_del_test_per_commit, total_del_commits, all_del_tests
        print(project)
        print("-----------------")
        VALIDATION_FILES_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/validation_diff_done_hydrated.csv"
        )

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")

            # Parse only deleted tests dataframe; Should select all rows
            deleted_tc_df = df[df["Final Results"] == "yes"]
            print("Total del tests: ", deleted_tc_df.shape[0])
            deleted_tests = list(deleted_tc_df["Removed Test Case"])
            all_del_tests = [*all_del_tests, *deleted_tests]

            # no. of deleted tests
            test_deletion_commits_df = deleted_tc_df["Hash"].value_counts().to_frame()
            test_deletion_commits_df = test_deletion_commits_df.reset_index()
            print(test_deletion_commits_df.head())
            test_deletion_commits_df = test_deletion_commits_df.rename(
                columns={"count": "Deleted Tests"},
                errors="raise",
            )

            print("Total del commits: ", test_deletion_commits_df.shape[0])
            print(
                "% del commits : ",
                (test_deletion_commits_df.shape[0] / total_commits[index]) * 100,
            )
            deleted_test_per_commits = list(test_deletion_commits_df["Deleted Tests"])
            total_del_commits += len(deleted_test_per_commits)
            all_data_del_test_per_commit = [
                *all_data_del_test_per_commit,
                *deleted_test_per_commits,
            ]
            print("Mean: ", np.mean(test_deletion_commits_df["Deleted Tests"]))
            print("Median: ", np.median(test_deletion_commits_df["Deleted Tests"]))
            print("Q1: ", np.percentile(test_deletion_commits_df["Deleted Tests"], 25))
            print("Q3: ", np.percentile(test_deletion_commits_df["Deleted Tests"], 75))
            print("Max: ", np.max(test_deletion_commits_df["Deleted Tests"]))
        print("================================")

    main(project)


print("--********-----")
print("All Projects")
print("----------")
print("Total del tests: ", len(all_del_tests))
print("Total del commits: ", total_del_commits)
print("% of del commits", (total_del_commits / np.sum(total_commits) * 100))
print("Mean: ", np.mean(all_data_del_test_per_commit))
print("Median: ", np.median(all_data_del_test_per_commit))
print("Q1: ", np.percentile(all_data_del_test_per_commit, 25))
print("Q3: ", np.percentile(all_data_del_test_per_commit, 75))
print("Max: ", np.max(all_data_del_test_per_commit))
