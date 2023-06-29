import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import (
    get_full_commit_url,
    parse_commit_as_hyperlink,
    get_change_id_from_commit_msg,
    get_bug_id_from_commit_msg
)

IO_DIR = "io/validationFiles4"
PROJECT = "cts"

def handle_print(df, filename):
    df = df.copy(deep=True)
    prev = {
                "Datetime": None,
                "Hash": None,
                "Commit Msg": None,
                "Filename": None,
                "Removed Test Case": None,
                "Manual Validation": None,
                "Final Results": None,
                "Ajay Manual Validation": None,
                "Suraj Manual Validation": None,
                "Ajay Comments": None,
                "Suraj Comments": None,
            }

    for index, row in df.iterrows():
        if index == 0:
            prev = {
                "Datetime": row["Datetime"],
                "Commit Msg": row["Commit Msg"],
                "Hash": row["Hash"],
                "Filename": row["Filename"],
                "Removed Test Case": row["Removed Test Case"],
                "Manual Validation": row["Manual Validation"],
                "Final Results": row["Final Results"],
                "Ajay Manual Validation": row["Ajay Manual Validation"],
                "Suraj Manual Validation": row["Suraj Manual Validation"],
                "Ajay Comments": row["Ajay Comments"],
                "Suraj Comments": row["Suraj Comments"],
            }

        else:
            if row["Hash"] == prev["Hash"]:
                row["Hash"] = ""
                row["Commit Msg"] = ""
                row["Datetime"] = ""

                if row["Filename"] == prev["Filename"]:
                    row["Filename"] = ""
                    row["Confidence"] = ""
                else:
                    prev["Filename"] = row["Filename"]

            else:
                prev["Hash"] = row["Hash"]
                prev["Datetime"] = row["Datetime"]
                prev["Commit Msg"] = prev["Commit Msg"]

                prev["Filename"] = row["Filename"]

            # if pd.isna(row["Manual Validation"]) or pd.isnull(row["Manual Validation"]):
            #     row["Manual Validation"] = prev["Manual Validation"]
            # else:
            #     prev["Manual Validation"] = row["Manual Validation"]

            # if pd.isna(row["Ajay Manual Validation"]) or pd.isnull(row["Ajay Manual Validation"]):
            #     row["Ajay Manual Validation"] = prev["Ajay Manual Validation"]
            # else:
            #     prev["Ajay Manual Validation"] = row["Ajay Manual Validation"]

            # if pd.isna(row["Suraj Manual Validation"]) or pd.isnull(row["Suraj Manual Validation"]):
            #     row["Suraj Manual Validation"] = prev["Suraj Manual Validation"]
            # else:
            #     prev["Suraj Manual Validation"] = row["Suraj Manual Validation"]

            # if pd.isna(row["Ajay Comments"]) or pd.isnull(row["Ajay Comments"]):
            #     row["Ajay Comments"] = prev["Ajay Comments"]
            # else:
            #     prev["Ajay Comments"] = row["Ajay Comments"]

            # if pd.isna(row["Suraj Comments"]) or pd.isnull(row["Suraj Comments"]):
            #     row["Suraj Comments"] = prev["Suraj Comments"]
            # else:
            #     prev["Suraj Comments"] = row["Suraj Comments"]

    df.to_csv(f"{IO_DIR}/{PROJECT}/{filename}", index=False)
    print(f"Generated {IO_DIR}/{PROJECT}/{filename}")
    
            
def main():
    VALIDATION_FILE = "validation_hydrated.csv"
    OUTPUT_FILE = "validation_hydrated_cleaned"

    full_file_path = Path(f"{IO_DIR}/{PROJECT}/{VALIDATION_FILE}")

    if not os.path.exists(f"{full_file_path}"):
        return
    
    df = pd.read_csv(f"{full_file_path}")
    print("Start Size:", df.shape)
    df = df.iloc[:, 0:11]


    # Step 1
    print("Step: 1")
    unique_changeid = []
    unique_changeid_hash = []
    to_be_dropped_commit_hash = []
    for index, row in df.iterrows():
        if "Change-Id: " in row["Commit Msg"]:
            change_id = get_change_id_from_commit_msg(row["Commit Msg"])
            # print(change_id)
            if change_id in unique_changeid:
                if row['Hash'] in unique_changeid_hash:
                    pass
                else:
                    if row["Hash"] not in to_be_dropped_commit_hash:
                        to_be_dropped_commit_hash.append(row["Hash"])
            else:
                unique_changeid.append(change_id)
                
                if row['Hash'] not in unique_changeid_hash:
                    unique_changeid_hash.append(row["Hash"])

    print("Commits to be dropped: ", len(to_be_dropped_commit_hash))
    
    
    for hash in to_be_dropped_commit_hash:
        to_be_dropped_index = df[(df["Hash"] == hash)].index
        df.drop(to_be_dropped_index, inplace=True)

    print("Step 1 Size:", df.shape)
    filename = OUTPUT_FILE + "1.csv"
    handle_print(df, filename)
    
    
    # Step 2
    print("Step 2")
    df['Commit Msg'] = df['Commit Msg'].apply(str.lower)
    unique_bugid = []
    unique_bugid_hash = []
    to_be_dropped_commit_hash = []
    for index, row in df.iterrows():
        bug_id = get_bug_id_from_commit_msg(row["Commit Msg"])
        if bug_id:
            if bug_id in unique_bugid:
                if row['Hash'] in unique_bugid_hash:
                    pass
                else:
                    if row["Hash"] not in to_be_dropped_commit_hash:
                        to_be_dropped_commit_hash.append(row["Hash"])
            else:
                unique_bugid.append(bug_id)
                
                if row['Hash'] not in unique_bugid_hash:
                    unique_bugid_hash.append(row["Hash"])

    print("Commits to be dropped: ", len(to_be_dropped_commit_hash))
    
    
    for hash in to_be_dropped_commit_hash:
        to_be_dropped_index = df[(df["Hash"] == hash)].index
        df.drop(to_be_dropped_index, inplace=True)
    
    print("Step 2 Size:", df.shape)
    filename = OUTPUT_FILE + "2.csv"
    handle_print(df, filename)


    # Step 3
    print("Step: 3")
    to_be_dropped_commit_hash = []
    for index, row in df.iterrows():
        if "merged from:" in row["Commit Msg"]:
            if row["Hash"] not in to_be_dropped_commit_hash:
                to_be_dropped_commit_hash.append(row["Hash"])
        

    print("Commits to be dropped: ", len(to_be_dropped_commit_hash))
    
    
    for hash in to_be_dropped_commit_hash:
        to_be_dropped_index = df[(df["Hash"] == hash)].index
        df.drop(to_be_dropped_index, inplace=True)

    print("Step 3 Size:", df.shape)
    filename = OUTPUT_FILE + "3.csv"
    handle_print(df, filename)


main()
