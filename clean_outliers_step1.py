import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import (
    get_full_commit_url,
    parse_commit_hash_by_project,
    get_change_id_from_commit_msg,
    get_bug_id_from_commit_msg,
)

IO_DIR = "io/artifacts"


# For commons-lang and joda-time
commits_to_ignore = {
    "commons-lang": [
        "4f3b6e55f86c8b59ea9b3991ca055c3905eb05a1",
    ],
    "joda-time": ["72b22654962284bac59c2777131b42a2d1f53228"],
}

for project in ["commons-lang", "joda-time", "cts"]:
    full_input_file_path = Path(f"{IO_DIR}/{project}/hydrated_{project}-step1.csv")
    full_output_file_path = Path(
        f"{IO_DIR}/{project}/hydrated_{project}-step1_refined.csv"
    )

    if not os.path.exists(f"{full_input_file_path}"):
        print(f"File does not exist: {full_input_file_path}")
        continue

    df = pd.read_csv(f"{full_input_file_path}")
    print("Start Size:", df.shape)
    df = df.iloc[:, 0:11]

    if project != "cts":
        to_ignore_commits = list(
            map(
                lambda each: parse_commit_hash_by_project(
                    project,
                    each,
                ),
                commits_to_ignore[project],
            )
        )
        print(to_ignore_commits)
        df = df[~df["Hash"].isin(to_ignore_commits)]

    else:
        # Check for duplicated change id
        print("Step: 1")
        unique_changeid = []
        unique_changeid_hash = []
        to_be_dropped_commit_hash = []
        for index, row in df.iterrows():
            if "Change-Id: " in row["Commit Msg"]:
                change_id = get_change_id_from_commit_msg(row["Commit Msg"])
                # print(change_id)
                if change_id in unique_changeid:
                    if row["Hash"] in unique_changeid_hash:
                        pass
                    else:
                        if row["Hash"] not in to_be_dropped_commit_hash:
                            to_be_dropped_commit_hash.append(row["Hash"])
                else:
                    unique_changeid.append(change_id)

                    if row["Hash"] not in unique_changeid_hash:
                        unique_changeid_hash.append(row["Hash"])

        print("Commits to be dropped: ", len(to_be_dropped_commit_hash))

        for hash in to_be_dropped_commit_hash:
            to_be_dropped_index = df[(df["Hash"] == hash)].index
            df.drop(to_be_dropped_index, inplace=True)

        print("Step 1 Size:", df.shape)

        # Check for merged from
        print("Step: 2")
        to_be_dropped_commit_hash = []
        for index, row in df.iterrows():
            if "merged from:" in row["Commit Msg"]:
                if row["Hash"] not in to_be_dropped_commit_hash:
                    to_be_dropped_commit_hash.append(row["Hash"])

        print("Commits to be dropped: ", len(to_be_dropped_commit_hash))

        for hash in to_be_dropped_commit_hash:
            to_be_dropped_index = df[(df["Hash"] == hash)].index
            df.drop(to_be_dropped_index, inplace=True)

        print("Step 2 Size:", df.shape)

    # Finally export the refined dataframe
    print("Final Size:", df.shape)
    df.to_csv(f"{full_output_file_path}", index=False)
    print(f"Generated {full_output_file_path}")
