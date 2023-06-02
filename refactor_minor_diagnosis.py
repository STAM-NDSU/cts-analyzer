import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf

IO_DIR = "io/outputRevisedLatest/commons-math"

""" Step 1"""
OUTPUT_FILE = "commons-math_hydrated_step"
files = [
    {
        "filename": "commons-math-step1_01-01-2000_01-01-2023",
    },
    {
        "filename": "commons-math-step2_01-01-2000_01-01-2023",
    },
    {
        "filename": "commons-math-step3_01-01-2000_01-01-2023",
    },
]


def parse_files(files):
    return map(lambda file_data: file_data["filename"] + ".csv", files)


def get_sheet_name(filepath):
    return filepath.split("/")[0]


for file_index, filepath in enumerate(parse_files(files)):
    full_file_path = Path(f"{IO_DIR}/{filepath}")

    if os.path.exists(f"{full_file_path}"):
        df = pd.read_csv(f"{full_file_path}")

        df = df.iloc[:, 0:6]
        prev = {
            "Datetime": None,
            "Hash": None,
            "Commit Msg": None,
            "Filename": None,
            "Removed Test Case": None,
            "Confidence": None,
        }
        for index, row in df.iterrows():
            if index == 0:
                prev = {
                    "Datetime": row["Datetime"],
                    "Hash": row["Hash"],
                    "Commit Msg": row["Commit Msg"],
                    "Filename": row["Filename"],
                    "Removed Test Case": row["Removed Test Case"],
                    "Confidence": row["Confidence"],
                }

            else:
                if pd.isna(row["Datetime"]) or pd.isnull(row["Datetime"]):
                    row["Datetime"] = prev["Datetime"]
                else:
                    prev["Datetime"] = row["Datetime"]

                if pd.isna(row["Hash"]) or pd.isnull(row["Hash"]):
                    row["Hash"] = prev["Hash"]
                else:
                    prev["Hash"] = row["Hash"]

                if pd.isna(row["Commit Msg"]) or pd.isnull(row["Commit Msg"]):
                    row["Commit Msg"] = prev["Commit Msg"]
                else:
                    prev["Commit Msg"] = row["Commit Msg"]

                if pd.isna(row["Filename"]) or pd.isnull(row["Filename"]):
                    row["Filename"] = prev["Filename"]
                else:
                    prev["Filename"] = row["Filename"]

                if pd.isna(row["Removed Test Case"]) or pd.isnull(
                    row["Removed Test Case"]
                ):
                    row["Removed Test Case"] = prev["Removed Test Case"]
                else:
                    prev["Removed Test Case"] = row["Removed Test Case"]

                if pd.isna(row["Confidence"]) or pd.isnull(row["Confidence"]):
                    row["Confidence"] = prev["Confidence"]
                else:
                    prev["Confidence"] = row["Confidence"]
        df.to_csv(f"{IO_DIR}/{OUTPUT_FILE}_{file_index+1}.csv", index=False)


""" Step 2"""


file1 = "io/outputRevisedLatest/commons-math/commons-math_hydrated_step_1.csv"
file2 = "io/outputRevisedLatest/commons-math/commons-math_hydrated_step_2.csv"
file3 = "io/outputRevisedLatest/commons-math/commons-math_hydrated_step_3.csv"

writer = pd.ExcelWriter(f"{IO_DIR}/refactor-minor_steps-diff", engine="xlsxwriter")
with open(file1, "r") as a, open(file2, "r") as b, open(file3, "r") as c:
    file1 = list(csv.reader(a, delimiter=","))
    file2 = list(csv.reader(b, delimiter=","))
    file3 = list(csv.reader(c, delimiter=","))
    print(len(list(file3)), len(list(file2)), len(list(file1)))
    # # diff step 1 and step 2
    # alter = []
    # for each1 in file1:
    #     if each1[1] != '':
    #         match_found = False

    #         all_related = filter(lambda each: each[1] == each1[1], file2)
    #         for each2 in all_related:
    #             if each1[4] == each2[4]:
    #                 match_found = True
    #                 break
    #         if not match_found:
    #             alter.append([each1[1], each1[3], each1[4]])

    # new_df = pd.DataFrame(alter, columns=["Hash", "Filename", "TestCase"])
    # new_df.to_excel(writer, sheet_name="diff step1 and step2", index=False)

    # diff step 2 and step 3
    alter = []
    for index, each1 in enumerate(file2):
        if each1[1] == "" or each1[1] == "Hash":
            continue

        match_found = False
        all_related = list(filter(lambda x: x[1] == each1[1], file3))

        # if index == 5:
        #     print(all_related)

        for each2 in all_related:
            if each1[4] == each2[4]:
                match_found = True
                break

        if not match_found:
            alter.append([each1[1], each1[3], each1[4]])

    new_df = pd.DataFrame(alter, columns=["Hash", "Filename", "TestCase"])
    new_df.to_excel(writer, sheet_name="diff step2 and step3", index=False)

writer.close()
