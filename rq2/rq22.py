"""
Computes test-deletion commits stat across projects
"""


import os.path
from pathlib import Path
import pandas as pd
import random
import csv

import sys

sys.path.append("../")

from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import strip_commit_url
from datetime import datetime
import os


projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]
output_path = "../io/validationFiles/rq22_stat.csv"
new_df = pd.DataFrame()
new_df = pd.DataFrame(
    columns=[
        "Project",
        "Deleting Single Testcase",
        "Deleting Multiple Testcase",
        "Deleting Testcase Only",
        "Deleting Single Testclass",
        "Deleting Multiple Testclass",
    ]
)

for project in projects_list:

    def main(project):
        global new_df

        print(project)
        print("---------------")
        IO_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(f"{IO_DIR}/{PROJECT}/hydrated_rq_2.csv")

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")
            deleted_tc_df_clone = df.copy(deep=True)

            # step 1
            commits_deleting_single_testcase = 0
            commits_deleting_mul_testcase = 0
            # step 2
            commits_deleting_only_testcases = 0
            commits_deleting_single_testclass = 0
            commits_deleting_mul_testclass = 0

            commits = list(deleted_tc_df_clone["Hash"].unique())
            print(project, "total commits ", len(commits))
            for commit in commits:
                # compute if commit deletes multiple testcases
                matching_hash_df = deleted_tc_df_clone[
                    deleted_tc_df_clone["Hash"] == commit
                ]
                
                if matching_hash_df.shape[0] > 1:
                    commits_deleting_mul_testcase += 1
                elif matching_hash_df.shape[0] == 1:
                    commits_deleting_single_testcase += 1

                # compute if commit deletes multiple testclass if any
                deleted_with_whole_file_df = matching_hash_df[
                    matching_hash_df["Deleted With Whole File"] == "yes"
                ]
                not_deleted_with_whole_file_df = matching_hash_df[
                    matching_hash_df["Deleted With Whole File"] == "no"
                ]

                del_with_whole_filepaths = list(deleted_with_whole_file_df["Filepath"].unique())
                not_del_with_whole_filepaths = list(not_deleted_with_whole_file_df["Filepath"].unique())
                if len(del_with_whole_filepaths) > 1:
                    commits_deleting_mul_testclass += 1
                elif len(del_with_whole_filepaths) == 1:
                    commits_deleting_single_testclass += 1
                else:
                    if len(not_del_with_whole_filepaths) > 0:
                        commits_deleting_only_testcases += 1

            new_df.loc[len(new_df.index)] = [
                project,
                commits_deleting_single_testcase,
                commits_deleting_mul_testcase,
                commits_deleting_only_testcases,
                commits_deleting_single_testclass,
                commits_deleting_mul_testclass,
            ]

    main(project)

print(new_df)
new_df.to_csv(output_path, index=False)
print(f"Generated {output_path}")
print("===================================================")
