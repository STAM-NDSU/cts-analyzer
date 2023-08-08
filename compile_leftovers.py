import os.path
from pathlib import Path
import pandas as pd


root_dir = "./io/validationFiles/"
output_file = "leftovers.xlsx"

projects_list = [
    "commons-lang",
    "commons-math",
    "pmd",
    "jfreechart",
    "gson",
    "joda-time",
    "cts",
]

writer = pd.ExcelWriter(f"{root_dir}/{output_file}", engine="xlsxwriter")
for project in projects_list:
    file_path = Path(f"{root_dir}/{project}/validation_diff_leftovers.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(f"{file_path}")
        df.to_excel(writer, sheet_name=project, index=False)
    else: 
        print("Error")

writer.close()
print(f"Generated {root_dir}/{output_file}")
