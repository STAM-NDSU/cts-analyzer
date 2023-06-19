import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf

IO_DIR = "io/validationFiles4/cts"
OUTPUT_FILE = "validation_diff"

step3_file = "io/outputRevisedLatest4/cts/hydrated_cts-step3.csv"
validated_file = "io/validationFiles4/cts/validation_hydrated.csv"

base_columns = [
    "Datetime",
    "Hash",
    "Commit Msg",
    "Filename",
    "Removed Test Case",
]

columns = [
    *base_columns,
    # "Confidence",
    "Manual Validation",
    "Final Results",
    "Ajay Manual Validation",
    "Suraj Manual Validation",
    "Ajay Comments",
    "Suraj Comments",
]

# writer = pd.ExcelWriter(f"{IO_DIR}/{OUTPUT_FILE}", engine="xlsxwriter")
with open(step3_file, "r") as a, open(validated_file, "r") as b:
    step3_file = list(csv.reader(a, delimiter=","))
    validated_file = list(csv.reader(b, delimiter=","))
    step3_file.pop(0)
    validated_file.pop(0)

    print(len(step3_file), len(validated_file))

    # diff
    alter = []
    matched = []
    for step3_record in step3_file:
        # Ignore Filepath and Check Annot
        format_step3_record = [
            step3_record[0],
            step3_record[1],
            step3_record[2],
            step3_record[4],
            step3_record[5],
        ]

        match_found = False
        all_validated_and_related = list(
            filter(lambda each: each[1] == format_step3_record[1], validated_file)
        )
        # print(all_validated_and_related)
        # print(all_validated_and_related)
        for validated_record in all_validated_and_related:
            # Ignore Confidence
            print(validated_record)

            format_step3_record = [
                step3_record[0],
                step3_record[1],
                step3_record[2],
                step3_record[4],
                step3_record[5],
            ]

            if (
                format_step3_record[3] == validated_record[3]
                and format_step3_record[4] == validated_record[4]
            ):
                match_found = True
                matched.append([*validated_record])
                break
        if not match_found:
            alter.append([*format_step3_record])

    print(len(alter), len(matched))
    alter_df = pd.DataFrame(
        alter,
        columns=base_columns,
    )
    # alter_df.to_excel(writer, sheet_name="leftovers", index=False)
    alter_df.to_csv(f"{IO_DIR}/{OUTPUT_FILE}_leftovers_hydrated.csv", index=False)

    matched_df = pd.DataFrame(matched, columns=columns)
    # matched_df.to_excel(writer, sheet_name="done", index=False)
    matched_df.to_csv(f"{IO_DIR}/{OUTPUT_FILE}_done_hydrated.csv", index=False)

# writer.close()
