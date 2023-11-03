"""
Computes deleted tests stat across projects
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
output_path = "../io/validationFiles/rq21_stat.csv"
new_df = pd.DataFrame(
    columns=[
        "Project",
        "Deleted With Source Code",
        "Not Deleted With Source Code",
        "Deleted With Whole File",
        "Not Deleted With Whole File",
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
            print("Size", df.shape[0])
            deleted_tc_df_clone = df.copy(deep=True)
            # no. of testcases grouped by deleted with source code
            grouped_deleted_tc_by_source_df = deleted_tc_df_clone.groupby(
                "Deleted With Source Code"
            )["Hash"].count()
            grouped_deleted_tc_by_source_df = (
                grouped_deleted_tc_by_source_df.reset_index()
            )

            del_w_sc = grouped_deleted_tc_by_source_df.iloc[1]["Hash"]
            nt_del_w_sc = grouped_deleted_tc_by_source_df.iloc[0]["Hash"]
            print(grouped_deleted_tc_by_source_df)

            # deleted with test class file
            grouped_deleted_tc_by_file_df = deleted_tc_df_clone.groupby(
                "Deleted With Whole File"
            )["Hash"].count()
            grouped_deleted_tc_by_file_df = grouped_deleted_tc_by_file_df.reset_index()

            del_w_wf = grouped_deleted_tc_by_file_df.iloc[1]["Hash"]
            nt_del_w_wf = grouped_deleted_tc_by_file_df.iloc[0]["Hash"]

            new_df.loc[len(new_df.index)] = [
                project,
                del_w_sc,
                nt_del_w_sc,
                del_w_wf,
                nt_del_w_wf,
            ]

    main(project)

print(new_df)
new_df.to_csv(output_path, index=False)
print(f"Generated {output_path}")
print("===================================================")
