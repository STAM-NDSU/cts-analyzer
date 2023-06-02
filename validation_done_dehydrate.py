import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import get_full_commit_url, parse_commit_as_hyperlink

IO_DIR = "io/validationFiles4"
PROJECT = "gson"
OUTPUT_FILE = "validation_diff_done"
files = [
    {
        "filename": "validation_diff_done_hydrated"
    }
]

def parse_files(files):
    return map(lambda file_data: file_data["filename"] + ".csv", files)

for file_index, filepath in enumerate(parse_files(files)):
    full_file_path = Path(f"{IO_DIR}/{PROJECT}/{filepath}")

    if os.path.exists(f"{full_file_path}"):
        df = pd.read_csv(f"{full_file_path}")
        
        df = df.iloc[:, 0:12]
        prev = {
            "Datetime": None,
            "Hash": None,
            "Commit Msg": None,
            "Filename": None,
            "Removed Test Case": None,
            "Confidence": None,
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
                    "Confidence": row["Confidence"],
                    "Manual Validation": row["Manual Validation"],
                    "Final Results": row["Final Results"],
                    "Ajay Manual Validation": row["Ajay Manual Validation"],
                    "Suraj Manual Validation": row["Suraj Manual Validation"],
                    "Ajay Comments": row["Ajay Comments"],
                    "Suraj Comments": row["Suraj Comments"],
                }
               
            else:
               
                if row["Hash"] == prev["Hash"]:
                    row["Hash"] = ''
                    row["Commit Msg"] = ''
                    row["Datetime"] = ''
                    
                    if row["Filename"] == prev["Filename"]:
                        row["Filename"] = ''
                        row["Confidence"] = ''
                    else:
                        prev["Filename"] = row["Filename"]
                        prev["Confidence"] = row["Confidence"]
                    
                else:
                    prev["Hash"] = row["Hash"]
                    prev["Datetime"] = row["Datetime"]
                    prev["Commit Msg"] = prev["Commit Msg"]
                    
                    prev["Filename"] = row["Filename"]
                    prev["Confidence"] = row["Confidence"]
             
                
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
                    
        df.to_csv(f"{IO_DIR}/{PROJECT}/{OUTPUT_FILE}.csv", index=False)

