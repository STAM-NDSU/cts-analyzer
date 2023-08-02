"""
Prettify results from rq12.py to export in latex
"""
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

import sys

# Redirect console ouput to a file
sys.stdout = open("./stats/all_repos_version_stat_prettify.txt", "w")

projects_list = [
    "commons-lang",
    "commons-math",
    "pmd",
    "jfreechart",
    "gson",
    "joda-time",
    "cts",
]


for project in projects_list:

    def main(project):
        print(project)
        print("-----------------")
        VALIDATION_FILES_DIR = "io/validationFiles"
        PROJECTS_DIR = "io/projects"
        PROJECT = project
        stat_version_test_deletions_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/stat_version_test_deletion.csv"
        )

        if os.path.exists(f"{stat_version_test_deletions_file_path}"):
            df = pd.read_csv(f"{stat_version_test_deletions_file_path}")
            tags = []
            ranges = []
            commits = []
            test_deletion_commits = []
            total_deleted_tests = []
            for index, row in df.iterrows():
                if index == 0:
                    continue
                tag = row["Tag"].split("/")[-1].replace("^{}", "").replace("v", "")
                tag = tag.replace("LANG_", "").replace(
                    "commons-lang-", ""
                )  # commons-lang
                tag = tag.replace("_", ".")
                tag = (
                    tag.replace("gson-", "")
                    .replace("parent-", "")
                    .replace("android-", "")
                )  # gson
                tag = tag.replace("MATH.", "").replace(
                    "commons-math-", ""
                )  # commons-math
                tag = (
                    tag.replace("android-", "").replace(".r1", "")
                )  # cts
                tags.append(tag)
                range = str(int(row["Range"])) if row["Range"] else "0"
                ranges.append(range)
                commit = str(int(row["Commits"])) if row["Commits"] else "0"
                commits.append(commit)
                test_deletion_commit = (
                    str(int(row["Test Deletion Commits"]))
                    if row["Test Deletion Commits"]
                    else "0"
                )
                test_deletion_commits.append(test_deletion_commit)
                total_deleted_test = (
                    str(int(row["Total Deleted Tests"]))
                    if row["Total Deleted Tests"]
                    else "0"
                )
                total_deleted_tests.append(total_deleted_test)

            print("Total versions: ", len(tags))
            tags_with_deleted_tests = []
            for index, each in enumerate(total_deleted_tests):
                if int(each) > 0:
                    tags_with_deleted_tests.append(
                        {"old_index": index, "total_deleted_tests": each}
                    )

            print("Total versions with deleted tests", len(tags_with_deleted_tests))
            str1 = ""
            for index, tag_info in enumerate(tags_with_deleted_tests):
                if index == 0:
                    str1 = f'{tags[tag_info["old_index"]]}({ranges[tag_info["old_index"]]}) \\textrightarrow {tag_info["total_deleted_tests"]}({test_deletion_commits[tag_info["old_index"]]})'
                else:
                    str1 = str1 + f',{tags[tag_info["old_index"]]}({ranges[tag_info["old_index"]]}) \\textrightarrow {tag_info["total_deleted_tests"]}({test_deletion_commits[tag_info["old_index"]]})'
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
