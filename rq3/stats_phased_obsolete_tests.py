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
]
output_path = "../io/validationFiles/stats_phased_obsolete_tests.csv"
new_df = pd.DataFrame(
    columns=[
        "Project",
        "Concurrent Obsolete",
        "Phased Obsolete",
        "Others",
        "Decided",
        "Undecided"
    ]
)


for project in projects_list:

    def main(project):
        global new_df

        print(project)
        print("---------------")
        IO_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(f"{IO_DIR}/{PROJECT}/hydrated_rq_2_with_deletion_type.csv")

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")
            print("Size", df.shape[0])
            deleted_tc_df_clone = df.copy(deep=True)
            
            # tests grouped by deletion type i.e concurrent obsolete, phased or not obsolete
            grouped_by_del_type_df = deleted_tc_df_clone.groupby(
                "Type"
            )["Hash"].count()
            deletion_type_data = grouped_by_del_type_df.to_dict()
           
            
             # tests grouped by is obsolete dececion type i.e decided(100% surity) or undecided
            grouped_by_decision_df = deleted_tc_df_clone.groupby(
                "Deleted With Source Code Decision"
            )["Hash"].count()
            decision_type_data = grouped_by_decision_df.to_dict()
            
            new_df.loc[len(new_df.index)] = [
                project,
                deletion_type_data.get("concurrent obsolete", 0),
               deletion_type_data.get("phased obsolete", 0),
               deletion_type_data.get("not obsolete", 0),
               decision_type_data.get("decided", 0),
               decision_type_data.get("undecided", 0),
            ]

    main(project)

print(new_df)
new_df.to_csv(output_path, index=False)
print(f"Generated {output_path}")
print("===================================================")
