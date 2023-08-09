import sys

sys.path.append("../")

import os.path
from pathlib import Path
import pandas as pd


root_dir = "../io/validationFiles"
output_file = "validation.xlsx"

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

writer = pd.ExcelWriter(f"{root_dir}/{output_file}", engine="xlsxwriter")
for project in projects_list:
    file_path = Path(f"{root_dir}/{project}/validation_diff_done.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(f"{file_path}")
        
        yes_validate_df = df[df['Final Results']=="yes"]
        print(project)
        print(df['Final Results'].value_counts())
        print("Total commits",  len(list(yes_validate_df["Hash"].dropna().unique())))
        print("Total testcases",  yes_validate_df.shape[0])
        print('--------')
        df.to_excel(writer, sheet_name=project, index=False)

writer.close()
print(f"Generated {root_dir}/{output_file}")

