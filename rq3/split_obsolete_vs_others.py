"""
We split confirmed obsolete tests, which could be concurrent and phased obsolete and rest of tests labelled as others. Others tests require further manual validation.
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

VALIDATION_DIR = "../io/validationFiles"

for project in projects_list:

    def main(project):
        global new_df

        print(project)
        print("---------------")
        IO_DIR = "../io/validationFiles"
        PROJECT = project
        full_input_file_path = Path(
            f"{IO_DIR}/{PROJECT}/hydrated_rq_2_with_deletion_type.csv"
        )

        if os.path.exists(f"{full_input_file_path}"):
            df = pd.read_csv(f"{full_input_file_path}")

            new_df = df[
                (df["Deleted With Source Code Decision"] == "decided")
                & (
                    (df["Type"] == "phased obsolete")
                    | (df["Type"] == "concurrent obsolete")
                )
            ]

            full_output_file_path = Path(f"{VALIDATION_DIR}/{project}/obsolete.csv")
            new_df.to_csv(f"{full_output_file_path}", index=False)
            print(f"Generated {full_output_file_path}")

            # Place `phased and concurrent obsolete` tests inside separate folder `obsolete` for better organization
            out_dir = Path(f"{VALIDATION_DIR}/obsolete")
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            new_df.to_csv(f"{out_dir}/obsolete.csv", index=False)
            print(f"Generated {out_dir}/obsolete.csv")

            new_df = df[
                ~(
                    (df["Deleted With Source Code Decision"] == "decided")
                    & (
                        (df["Type"] == "phased obsolete")
                        | (df["Type"] == "concurrent obsolete")
                    )
                )
            ]
            full_output_file_path = Path(f"{VALIDATION_DIR}/{project}/not_obsolete.csv")
            new_df.to_csv(f"{full_output_file_path}", index=False)
            print(f"Generated {full_output_file_path}")

            # Place `others` tests inside separate folder `others` for better organization
            out_dir = Path(f"{VALIDATION_DIR}/others/")
            if not os.path.exists(f"{out_dir}"):
                os.mkdir(out_dir)
            new_df.to_csv(f"{out_dir}/{PROJECT}.csv", index=False)
            print(f"Generated {out_dir}/{PROJECT}.csv")

    main(project)

print("===================================================")
