"""
Computes test-deletion stat across projects
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


projects_list = [
    "commons-lang",
    "commons-math",
    "pmd",
    "jfreechart",
    "gson",
    "joda-time",
    # "cts",
]


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%m/%d/%Y %H:%M:%S")
    d2 = datetime.strptime(d2, "%m/%d/%Y %H:%M:%S")
    return abs((d2 - d1).days)


for project in projects_list:

    def main(project):
        print(project)
        print("---------------")
        IO_DIR = "io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(
            f"{IO_DIR}/{PROJECT}/validation_diff_done_hydrated.csv"
        )
        deleted_tc_output_file_path = Path(
            f"{IO_DIR}/{PROJECT}/deleted_tc_hydrated.csv"
        )
        test_deletion_commits_file_path = Path(
            f"{IO_DIR}/{PROJECT}/test_deletion_commits.csv"
        )
        stat_test_deletion_commits_file_path = Path(
            f"{IO_DIR}/{PROJECT}/stat_test_deletion_commits.csv"
        )
        stat_deletion_commits_grouped_year_file_path = Path(
            f"{IO_DIR}/{PROJECT}/stat_test_deletion_commits_grouped_year.csv"
        )
        test_deletion_datetime_inbetweencommits_range_file_path = Path(
            f"{IO_DIR}/{PROJECT}/test_deletion_datetime_inbetweencommits_range.csv"
        )
        stat_test_deletion_datetime_range_file_path = Path(
            f"{IO_DIR}/{PROJECT}/stat_test_deletion_datetime_range.csv"
        )
        stat_test_deletion_inbetween_range_file_path = Path(
            f"{IO_DIR}/{PROJECT}/stat_test_deletion_inbetween_range.csv"
        )

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")

            df = df.iloc[:, 0:11]
            deleted_tc_df = df[df["Final Results"] == "yes"]
            deleted_tc_df.to_csv(deleted_tc_output_file_path, index=False)
            deleted_tc_df = deleted_tc_df.reset_index(
                drop=True
            )  # Reset index of deleted testcase dataframe
            print(f"Generated {deleted_tc_output_file_path}")

            # Group test deletion commits by  year
            deleted_tc_df_clone = deleted_tc_df.copy(deep=True)
            deleted_tc_df_clone["Datetime"] = pd.to_datetime(
                deleted_tc_df_clone["Datetime"], format="%m/%d/%Y %H:%M:%S"
            )
            # no. of testcases by year
            grouped_deleted_tc_df = deleted_tc_df_clone.groupby(
                deleted_tc_df_clone.Datetime.dt.year
            )["Hash"].count()
            grouped_deleted_tc_df = grouped_deleted_tc_df.reset_index()
            # no. of test deletion commits by year
            deleted_tc_df_clone2 =  deleted_tc_df_clone.drop_duplicates(subset='Hash', keep="first")
            grouped_deleted_tc_commit_df = deleted_tc_df_clone2.groupby(
                deleted_tc_df_clone.Datetime.dt.year
            )["Hash"].count()
            grouped_deleted_tc_commit_df= grouped_deleted_tc_commit_df.reset_index()
            new_df = pd.DataFrame()
            new_df["Datetime"] = grouped_deleted_tc_df['Datetime']
            new_df["Commit"] = grouped_deleted_tc_commit_df['Hash']
            new_df["Testcase"] = grouped_deleted_tc_df['Hash']
            stat_deletion_commits_grouped_year_df = new_df.reset_index()
            stat_deletion_commits_grouped_year_df.to_csv(
                stat_deletion_commits_grouped_year_file_path, index=False
            )
            print(f"Generated {stat_deletion_commits_grouped_year_file_path}")

            # Find total number of test cases deleted by commit
            test_deletion_commits_df = deleted_tc_df["Hash"].value_counts().to_frame()
            test_deletion_commits_df = test_deletion_commits_df.reset_index()
            test_deletion_commits_df = test_deletion_commits_df.rename(
                columns={"index": "Commit Hash", "Hash": "Total Test Cases"},
                errors="raise",
            )
            test_deletion_commits_df.to_csv(
                test_deletion_commits_file_path, index=False
            )
            print(f"Generated {test_deletion_commits_file_path}")

            # Group test deletion commits by frequency of deleted tests in the commit
            stat_deletion_commits_df = test_deletion_commits_df.groupby(
                ["Total Test Cases"]
            )["Commit Hash"].count()
            stat_deletion_commits_df = stat_deletion_commits_df.reset_index()
            stat_deletion_commits_df.to_csv(
                stat_test_deletion_commits_file_path, index=False
            )
            print(f"Generated {stat_test_deletion_commits_file_path}")

            prev = {
                "Datetime": None,
                "Hash": None,
            }

            test_deletion_datetime_inbetweencommits_range = []
            # Find time interval between test deletion commits
            for i, row in deleted_tc_df.iterrows():
                if i == 0:
                    prev["Datetime"] = row["Datetime"]
                    prev["Hash"] = row["Hash"]
                    test_deletion_datetime_inbetweencommits_range.append(
                        [row["Hash"], None, None]
                    )
                else:
                    if row["Hash"] == prev["Hash"]:
                        pass
                    else:
                        # Compute the difference in days
                        range = days_between(prev["Datetime"], row["Datetime"])
                        # Compute no of in-between commits
                        cmd = f'git log {strip_commit_url(prev["Hash"])}...{strip_commit_url(row["Hash"])} --pretty=oneline | wc -l'
                        current_state = os.getcwd()
                        os.chdir(f"./io/projects/{project}")
                        # os.system("sleep 1")
                        os.system(cmd + " > tmp")
                        no_of_commits = open("tmp", "r").read().replace("\n", "")
                        os.chdir(current_state)
                        test_deletion_datetime_inbetweencommits_range.append(
                            [row["Hash"], range, no_of_commits]
                        )

                        # Update the previous unique hash record
                        prev["Datetime"] = row["Datetime"]
                        prev["Hash"] = row["Hash"]

            test_deletion_datetime_inbetweencommits_range_df = pd.DataFrame(
                test_deletion_datetime_inbetweencommits_range,
                columns=["Hash", "Range", "Commits"],
            )
            test_deletion_datetime_inbetweencommits_range_df.to_csv(
                test_deletion_datetime_inbetweencommits_range_file_path, index=False
            )
            print(
                f"Generated {test_deletion_datetime_inbetweencommits_range_file_path}"
            )

            # Group test deletion commits by frequency of test deletion datetime range
            stat_test_deletion_datetime_range = (
                test_deletion_datetime_inbetweencommits_range_df.groupby(["Range"])[
                    "Hash"
                ].count()
            )
            stat_test_deletion_datetime_range = (
                stat_test_deletion_datetime_range.reset_index()
            )
            stat_test_deletion_datetime_range.to_csv(
                stat_test_deletion_datetime_range_file_path, index=False
            )
            print(f"Generated {stat_test_deletion_datetime_range_file_path}")

            # Group test deletion commits by frequency of in-between commits
            stat_test_deletion_inbetween_range = (
                test_deletion_datetime_inbetweencommits_range_df.groupby(["Commits"])[
                    "Hash"
                ].count()
            )
            stat_test_deletion_inbetween_range = (
                stat_test_deletion_inbetween_range.reset_index()
            )
            stat_test_deletion_inbetween_range.to_csv(
                stat_test_deletion_inbetween_range_file_path, index=False
            )
            print(f"Generated {stat_test_deletion_inbetween_range_file_path}")
            print("===================================================")

    main(project)
