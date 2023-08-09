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
            # call groupby method.
            grouped_deleted_tc_commit_df = deleted_tc_df.groupby("Author")
            # call agg method
            grouped_deleted_tc_commit_df = grouped_deleted_tc_commit_df.agg(
                {"Hash": "nunique"}
            ).reset_index()
            print(grouped_deleted_tc_commit_df)

            print("total commits", grouped_deleted_tc_commit_df["Hash"].sum())
            print("total testcases", test_deletion_commits_df["Total Test Cases"].sum())
            new_df = pd.DataFrame(columns=['Authors', "Commits", 'Deleted Tests'])

            for index, row in test_deletion_commits_df.iterrows():
                filter_df = grouped_deleted_tc_commit_df[
                    grouped_deleted_tc_commit_df["Author"] == row["Author"]
                ]

                new_df.loc[len(new_df.index)] = [
                    row["Author"],
                    filter_df.iloc[0]["Hash"],
                    row["Total Test Cases"],
                ]

            new_df.to_csv(stat_authors_test_deletions_file_path, index=False)
            print(f"Generated {stat_authors_test_deletions_file_path}")

    main(project)
