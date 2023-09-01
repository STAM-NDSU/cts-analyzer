import sys

sys.path.append("../")

import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
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


for project in projects_list:

    def main(project):
        ARTIFACTS_DIR = "../io/artifacts/" + project 
        VALIDATION_DIR = "../io/validationFiles/" + project 
        
        OUTPUT_FILE = "validation_diff"
        stepfile_columns = [
            "Datetime",
            "Hash",
            "Parent",
            "Author",
            "Commit Msg",
            "Filepath",
            "Filename",
            "Removed Test Case",
        ]
        validated_columns = [
            "Datetime",
            "Hash",
            "Parent",
            "Author",
            "Commit Msg",
            "Filepath",
            "Filename",
            "Removed Test Case",
            "Manual Validation",
            "Final Results",
            "Ajay Manual Validation",
            "Suraj Manual Validation",
            "Ajay Comments",
            "Suraj Comments",
        ]

        step3_file = (
            ARTIFACTS_DIR
            + "/hydrated_"
            + project
            + "-step3.csv"
        )
        validated_file = VALIDATION_DIR + "/validation_hydrated.csv"

        if os.path.exists(step3_file) and os.path.exists(validated_file):
            # writer = pd.ExcelWriter(f"{VALIDATION_DIR}/{project}/{OUTPUT_FILE}", engine="xlsxwriter")
            with open(step3_file, "r") as a, open(validated_file, "r") as b:
                step3_file = list(csv.reader(a, delimiter=","))
                validated_file = list(csv.reader(b, delimiter=","))
                step3_file.pop(0)
                validated_file.pop(0)

                # diff
                alter = []
                matched = []
                for step3_record in step3_file:
                    # Ignore Filepath and Check Annot
                    [
                        datetime,
                        hash,
                        parent,
                        author,
                        commit_msg,
                        filepath,
                        filename,
                        testcase,
                    ] = step3_record

                    match_found = False
                    all_validated_and_hash_matched = list(
                        filter(
                            lambda each: each[1] == hash,
                            validated_file,
                        )
                    )

                    for validated_record in all_validated_and_hash_matched:
                        [
                            v_datetime,
                            v_hash,
                            v_commit_msg,
                            v_filename,
                            v_testcase,
                            manual_validation,
                            *extra_info,
                        ] = validated_record

                        if (
                            filename == v_filename
                            and v_testcase == testcase
                            and (manual_validation == "yes" or manual_validation == "no" or manual_validation == "conflict")
                        ):
                            match_found = True
                            matched.append(
                                [
                                    *step3_record,
                                    manual_validation,
                                    *extra_info,
                                ]
                            )
                            break
                    if not match_found:
                        alter.append([datetime, hash, parent, author, commit_msg, filepath, filename, testcase])

                alter_df = pd.DataFrame(
                    alter,
                    columns=stepfile_columns,
                )
                # alter_df.to_excel(writer, sheet_name="leftovers", index=False)
                alter_df.to_csv(
                    f"{VALIDATION_DIR}/{OUTPUT_FILE}_leftovers_hydrated.csv",
                    index=False,
                )
                print(f"Generated {VALIDATION_DIR}/{OUTPUT_FILE}_leftovers_hydrated.csv")

                matched_df = pd.DataFrame(matched, columns=validated_columns)
                # matched_df.to_excel(writer, sheet_name="done", index=False)
                matched_df.to_csv(
                    f"{VALIDATION_DIR}/{OUTPUT_FILE}_done_hydrated.csv", index=False
                )
                print(f"Generated {VALIDATION_DIR}/{OUTPUT_FILE}_done_hydrated.csv")
            # writer.close()

        else:
            if not os.path.exists(step3_file):
                print("ERROR: Step 3 does not exist for project " + project)
            else:
                print("ERROR: Validation file does not exist for project " + project)

    main(project)
