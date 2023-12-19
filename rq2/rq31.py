"""
REVISED
Computes test-deletion commits(deleted tests, test class) stat across projects
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
output_path = "../io/validationFiles/rq31_stat.csv"
new_df = pd.DataFrame()
new_df = pd.DataFrame(
    columns=[
        "Project",
        "No of Commits Deleting Test Class",
        "No. of Test Class",
        "No. of tests",
        "No of Commits Deleting Single Test",
        "No. of tests",
        "No of Commits Deleting Multiple Test",
        "No. of tests",
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

            # case 1
            commits_deleting_testclass = 0
            no_of_deleted_testclass = 0
            no_of_tests_deleted_with_testclass = 0

            # case 2
            commits_deleting_single_testcase = 0
            no_of_deleted_single_testcase = 0

            # case 3
            commits_deleting_mul_testcase = 0
            no_of_deleted_multiple_testcase = 0
            
        
            commits = list(deleted_tc_df_clone["Hash"].unique())
           
            for commit in commits:
                matching_hash_df = deleted_tc_df_clone[
                    deleted_tc_df_clone["Hash"] == commit
                ]
                    
                # CASE 1
                # compute commits deleting test class and other stats(no. of classes, no. of tests deleted)
                deleted_with_whole_file_df = matching_hash_df[
                    matching_hash_df["Deleted With Whole File"] == "yes"
                ]
                del_with_whole_filepaths = list(
                    deleted_with_whole_file_df["Filepath"].unique()
                )
                
                if len(del_with_whole_filepaths) >= 1:
                    commits_deleting_testclass += 1
                    no_of_deleted_testclass += len(del_with_whole_filepaths)
                    no_of_tests_deleted_with_testclass += deleted_with_whole_file_df.shape[
                        0
                    ]

                # CASE 2 & 3 
                # compute commits deleting single and multiple tests and no.of tests deleted
                not_deleted_with_whole_file_df = matching_hash_df[
                    matching_hash_df["Deleted With Whole File"] == "no"
                ]
                no_of_tests_deleted = not_deleted_with_whole_file_df.shape[0]

                    
                if no_of_tests_deleted == 1:
                    commits_deleting_single_testcase += 1
                    no_of_deleted_single_testcase += 1
                elif no_of_tests_deleted > 1:
                    no_of_deleted_multiple_testcase += no_of_tests_deleted
                    commits_deleting_mul_testcase += 1
                else:
                    print("Oops")
                    pass

            new_df.loc[len(new_df.index)] = [
                project,
                commits_deleting_testclass,
                no_of_deleted_testclass,
                no_of_tests_deleted_with_testclass,
                commits_deleting_single_testcase,
                no_of_deleted_single_testcase,
                commits_deleting_mul_testcase,
                no_of_deleted_multiple_testcase,
            ]
            print(commits_deleting_testclass, commits_deleting_single_testcase, commits_deleting_mul_testcase)

    main(project)

# print(new_df)
new_df.to_csv(output_path, index=False)
print(f"Generated {output_path}")
print("===================================================")
