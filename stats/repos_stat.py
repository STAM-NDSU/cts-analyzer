"""
Computes test-deletion stat across projects version
"""
import sys

sys.path.append("../")

import os.path
from pathlib import Path
from datetime import datetime
import os
from dateutil.relativedelta import relativedelta


# Redirect console ouput to a file
sys.stdout = open("../stats/all_repos_stat.txt", "w")

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return relativedelta(d2, d1)


for project in projects_list:
    print(project)
    print("------------")

    last_commit_cmd = f'git log master --date=format:"%Y-%m-%d %H:%M:%S" --pretty=format:"%H _ %ad" --until="2023-01-01 00:00:000" | head  -1'
    first_commit_cmd = f'git log master --date=format:"%Y-%m-%d %H:%M:%S" --pretty=format:"%H _ %ad" --until="2023-01-01 00:00:000" | tail  -1'
    if project == "joda-time":
        last_commit_cmd = last_commit_cmd.replace("master", "main")
        first_commit_cmd = first_commit_cmd.replace("master", "main")
    current_state = os.getcwd()
    os.chdir(f"./../os-java-projects/{project}")
    os.system(last_commit_cmd + " > tmp")
    last_hash_datetime = open("tmp", "r").read().replace("\n", "")
    [last_hash, last_date] = last_hash_datetime.split("_")
    last_date = last_date.strip()
    os.system(first_commit_cmd + " > tmp")
    first_hash_datetime = open("tmp", "r").read().replace("\n", "")
    [first_hash, first_date] = first_hash_datetime.split("_")
    first_date = first_date.strip()
    os.chdir(current_state)
    print("last Hash:", first_hash[:7])
    print("last Date:", first_date)
    print("last Hash:", last_hash[:7])
    print("last Date:", last_date)
    time_diff = days_between(first_date, last_date)
    print(
        "Diff:",
        time_diff.years,
        "years",
        time_diff.months,
        "months",
        time_diff.days,
        "days",
    )
    print("=========================")
