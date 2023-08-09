import os.path
from pathlib import Path
import pandas as pd

# Customize for required projects

root_dir = "../io/validationFiles/"
output_file = "authors_info.xlsx"

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
    file_path = Path(f"{root_dir}/{project}/stat_authors_test_deletions.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(f"{file_path}")
        df.to_excel(writer, sheet_name=project, index=False)

writer.close()