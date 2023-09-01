"""
Prettify results from rq12.py to export in latex
"""
import sys

sys.path.append("../")
# Redirect console ouput to a file
sys.stdout = open("../stats/all_repos_version_stat_prettify.txt", "w")

import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import strip_commit_url
from datetime import datetime
import os
import json
from rq12 import prettify_tag


projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

for project in projects_list:

    def main(project):
        print(project)
        print("-----------------")
        VALIDATION_FILES_DIR = "../io/validationFiles"
        PROJECT = project
        stat_version_test_deletions_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/stat_version_test_deletion.csv"
        )

        if os.path.exists(f"{stat_version_test_deletions_file_path}"):
            df = pd.read_csv(f"{stat_version_test_deletions_file_path}")
            print("Total versions: ", len(df["Tag"]))
            tags_with_deleted_tests_df = df[df["Total Deleted Tests"] > 0]

            print("Total versions with deleted tests", len(tags_with_deleted_tests_df))
            str1 = ""
            for index, row in tags_with_deleted_tests_df.iterrows():
                if index != 0:
                    str1 = str1 + ","

                str1 = (
                    str1
                    + f'{row["Tag"]}({row["Range"]}) \\textrightarrow {row["Total Deleted Tests"]}({row["Test Deletion Commits"]})'
                )

            # print("Tag")
            # print((',').join(tags))
            # print("Range")
            # print((',').join(ranges))
            # print("Commits")
            # print((',').join(commits))
            # print("Test Deletion Commits")
            # print((',').join(test_deletion_commits))
            # print("Total Deleted Tests")
            # print((',').join(total_deleted_tests))
            print(str1)
            print("=====================================")

    main(project)
