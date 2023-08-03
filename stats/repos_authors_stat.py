"""
Computes test-deletion stat across projects version
"""

import os.path
from pathlib import Path
import pandas as pd
import os
import json


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
        VALIDATION_FILES_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/validation_diff_done_hydrated.csv"
        )
        stat_authors_test_deletions_file_path = Path(
            f"{VALIDATION_FILES_DIR}/{PROJECT}/stat_authors_test_deletions.csv"
        )

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")

            # Parse only deleted tests dataframe; Should select all rows
            deleted_tc_df = df[df["Final Results"] == "yes"]

            # no. of deleted tests
            test_deletion_commits_df = deleted_tc_df["Author"].value_counts().to_frame()
            test_deletion_commits_df = test_deletion_commits_df.reset_index()
            test_deletion_commits_df = test_deletion_commits_df.rename(
                columns={"index": "Author", "Author": "Total Test Cases"},
                errors="raise",
            )
            
            # no. of test deletion commits
            deleted_tc_df_clone2 = deleted_tc_df.drop_duplicates(
                subset="Hash", keep="first"
            )
            grouped_deleted_tc_commit_df = deleted_tc_df_clone2.groupby("Author")[
                "Hash"
            ].count()
            grouped_deleted_tc_commit_df = grouped_deleted_tc_commit_df.reset_index()
            
            new_df = pd.DataFrame()
            new_df["Author"] = test_deletion_commits_df["Author"]
            new_df["Commit"] = grouped_deleted_tc_commit_df["Hash"]
            new_df["Total Test Cases"] = test_deletion_commits_df["Total Test Cases"]

            new_df.to_csv(stat_authors_test_deletions_file_path, index=False)
            print(f"Generated {stat_authors_test_deletions_file_path}")

    main(project)
