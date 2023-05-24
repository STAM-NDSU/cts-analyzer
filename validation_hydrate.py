# WARNING: Make sure .env is correct set to desired Project

import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import get_full_commit_url, parse_commit_as_hyperlink

IO_DIR = "io/validationFiles3/pmd"
OUTPUT_FILE = "pmd_validation_hydrated"
files = [
    {
        "filename": "pmd_validated"
    }
]

def parse_files(files):
    return map(lambda file_data: file_data["filename"] + ".csv", files)

for file_index, filepath in enumerate(parse_files(files)):
    full_file_path = Path(f"{IO_DIR}/{filepath}")

    if os.path.exists(f"{full_file_path}"):
        df = pd.read_csv(f"{full_file_path}")
        
        df = df.iloc[:, 0:12]
        prev = {
            "DATETIME": None,
            "HASH": None,
            "COMMIT MSG": None,
            "FILENAME": None,
            "REMOVED TEST CASE": None,
            "CONFIDENCE": None,
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
                    "DATETIME": row["DATETIME"],
                    "COMMIT MSG": row["COMMIT MSG"],
                    "FILENAME": row["FILENAME"],
                    "REMOVED TEST CASE": row["REMOVED TEST CASE"],
                    "CONFIDENCE": row["CONFIDENCE"],
                    "Manual Validation": row["Manual Validation"],
                    "Final Results": row["Final Results"],
                    "Ajay Manual Validation": row["Ajay Manual Validation"],
                    "Suraj Manual Validation": row["Suraj Manual Validation"],
                    "Ajay Comments": row["Ajay Comments"],
                    "Suraj Comments": row["Suraj Comments"],
                }
                prev["HASH"] = parse_commit_as_hyperlink(label=row["HASH"],
                                                        url=get_full_commit_url(row["HASH"]))
                row["HASH"] = prev["HASH"]
            else:
                if pd.isna(row["DATETIME"]) or pd.isnull(row["DATETIME"]):
                    row["DATETIME"] = prev["DATETIME"]
                else:
                    prev["DATETIME"] = row["DATETIME"]

                if pd.isna(row["HASH"]) or pd.isnull(row["HASH"]):
                    row["HASH"] = prev["HASH"]
                else:
                    prev["HASH"] = parse_commit_as_hyperlink(label=row["HASH"],
                                                        url=get_full_commit_url(row["HASH"]))
                    row["HASH"] = prev["HASH"]
                    
                if pd.isna(row["COMMIT MSG"]) or pd.isnull(row["COMMIT MSG"]):
                    row["COMMIT MSG"] = prev["COMMIT MSG"]
                else:
                    prev["COMMIT MSG"] = row["COMMIT MSG"]

                if pd.isna(row["FILENAME"]) or pd.isnull(row["FILENAME"]):
                    row["FILENAME"] = prev["FILENAME"]
                else:
                    prev["FILENAME"] = row["FILENAME"]

                if pd.isna(row["REMOVED TEST CASE"]) or pd.isnull(
                    row["REMOVED TEST CASE"]
                ):
                    row["REMOVED TEST CASE"] = prev["REMOVED TEST CASE"]
                else:
                    prev["REMOVED TEST CASE"] = row["REMOVED TEST CASE"]

                if pd.isna(row["CONFIDENCE"]) or pd.isnull(row["CONFIDENCE"]):
                    row["CONFIDENCE"] = prev["CONFIDENCE"]
                else:
                    prev["CONFIDENCE"] = row["CONFIDENCE"]
                
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
                    
        df.to_csv(f"{IO_DIR}/{OUTPUT_FILE}.csv", index=False)

