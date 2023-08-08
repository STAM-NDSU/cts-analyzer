import os.path
from pathlib import Path
import pandas as pd


import os.path
from pathlib import Path
import pandas as pd
import sys

sys.path.append("../")
# Redirect console ouput to a file
sys.stdout = open("../stats/all_repos_steps_stat.txt", "w")

all_data = [[], [], [], [], [], [], []]

# For step 1,2,3

root_dir = ""


projects = [
    {
        "project": "commons-lang",
        "files": [
            "commons-lang-step1_refined",
            "commons-lang-step2",
            "commons-lang-step3",
        ],
    },
    {
        "project": "gson",
        "files": [
            "gson-step1",
            "gson-step2",
            "gson-step3",
        ],
    },
    {
        "project": "commons-math",
        "files": [
            "commons-math-step1",
            "commons-math-step2",
            "commons-math-step3",
        ],
    },
    {
        "project": "jfreechart",
        "files": [
            "jfreechart-step1",
            "jfreechart-step2",
            "jfreechart-step3",
        ],
    },
    {
        "project": "joda-time",
        "files": [
            "joda-time-step1_refined",
            "joda-time-step2",
            "joda-time-step3",
        ],
    },
    {
        "project": "pmd",
        "files": [
            "pmd-step1",
            "pmd-step2",
            "pmd-step3",
        ],
    },
    {
        "project": "cts",
        "files": [
            "cts-step1_refined",
            "cts-step2",
            "cts-step3",
        ],
    },
]


def parse_filename(file, project):
    return "../io/artifacts/" + project + "/hydrated_" + file + ".csv"


for p_index, project_info in enumerate(projects):
    files = project_info["files"]
    project = project_info["project"]

    step_data = []
    for index, filename in enumerate(files):
        file_path = Path(f"{parse_filename(filename, project)}")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            total_commits = len(list(df["Hash"].dropna().unique()))
            total_testcases = df.shape[0]
            step_data = [*step_data, total_commits, total_testcases]
        else:
            print("Error: path not found ", file_path)

    all_data[p_index] = [project, *step_data]


# For validation step

for p_index, project_info in enumerate(projects):
    project = project_info["project"]
    file_path = Path(
        f"../io/validationFiles/{project}/validation_diff_done_hydrated.csv"
    )
    if os.path.exists(file_path):
        df = pd.read_csv(f"{file_path}")

        yes_validate_df = df[df["Final Results"] == "yes"]
        total_commits = len(list(yes_validate_df["Hash"].dropna().unique()))
        total_testcases = yes_validate_df.shape[0]
        all_data[p_index] = [*all_data[p_index], total_commits, total_testcases]


# print all stat numbers
for each in all_data:
    str1 = ""
    for i, ele in enumerate(each):
        if i == 0:
            str1 = str(ele)
        else:
            str1 += "," + str(ele)
    print(str1)
