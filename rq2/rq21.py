"""
Computes test-deletion stat across projects
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
    "commons-math",
    "pmd",
    "jfreechart",
    "gson",
    "joda-time",
    "cts",
]
output_path = "../io/validationFiles/rq21_stat.csv"
new_df = pd.DataFrame(columns=["Project", "Hash", "Deleted With Whole File", "Deleted With Source Code"])

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
            # no. of testcases grouped by deleted with source code
            grouped_deleted_tc_by_source_df = deleted_tc_df_clone.groupby(
                "Deleted With Source Code"
            )["Hash"].count()
            grouped_deleted_tc_by_source_df = grouped_deleted_tc_by_source_df.reset_index()
           
            grouped_deleted_tc_by_source_df["Project"] = project
            grouped_deleted_tc_by_source_df["Deleted With Whole File"] = ""
            print(grouped_deleted_tc_by_source_df)
            # new_df["Project"] = project
            # new_df["Deleted With Source Code"] = grouped_deleted_tc_df["Hash"]
            # new_df["Not Deleted With Source Code"] = grouped_deleted_tc_df["Hash"]

            # deleted with test class file
            grouped_deleted_tc_by_file_df = deleted_tc_df_clone.groupby(
                "Deleted With Whole File"
            )["Hash"].count()
            grouped_deleted_tc_by_file_df = grouped_deleted_tc_by_file_df.reset_index()
           
            grouped_deleted_tc_by_file_df["Project"] = project
            grouped_deleted_tc_by_file_df["Deleted With Source Code"] = ""
            print(grouped_deleted_tc_by_file_df)
            
            new_df = pd.concat([new_df, grouped_deleted_tc_by_source_df, grouped_deleted_tc_by_file_df], ignore_index = True)
            
    main(project)

print(new_df)
new_df.to_csv(output_path, index=False)
print(f"Generated {output_path}")
print("===================================================")
