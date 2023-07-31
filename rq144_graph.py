"""
Generate box plot for no. of deleted tests in commit [rq1]
"""
import os.path
from pathlib import Path
import pandas as pd
import random
import csv
from analyzer.helpers import export_to_csv
import analyzer.config as conf
from analyzer.utils import strip_commit_url
from datetime import datetime
import os
import json
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.dates as mdates


OUT_DIR = 'io/rq1/figures/'
# Set the figure size
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
# Set colors
colors = [
    "magenta",
    "blue",
    "green",
    "red",
    "cyan",
    "brown",
    # 'violet'
]
projects_list = [
    "commons-lang",
    "commons-math",
    "pmd",
    "jfreechart",
    "gson",
    "joda-time",
    # "cts",
]

fig, ax = plt.subplots(
     figsize=(20,8),
)
for index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        IO_DIR = "io/validationFiles"
        PROJECT = project
        stat_test_deletion_commits_grouped_year_file_path = Path(
            f"{IO_DIR}/{PROJECT}/stat_test_deletion_commits_grouped_year.csv"
        )

        if os.path.exists(f"{stat_test_deletion_commits_grouped_year_file_path}"):
            df = pd.read_csv(f"{stat_test_deletion_commits_grouped_year_file_path}")
            df["Datetime"] = pd.to_datetime(df["Datetime"], format="%Y")
            print(df["Datetime"])
            ax.plot(df["Datetime"], df["Testcase"], color=colors[index], label=project )

    main(project)


plt.xlabel("Year")
plt.ylabel("No. of tests deleted")

half_year_locator = mdates.MonthLocator(interval=24)
year_month_formatter = mdates.DateFormatter("%Y") # four digits for year, two for month

ax.xaxis.set_major_locator(half_year_locator)
ax.xaxis.set_major_formatter(year_month_formatter) # formatter for major axis only
ax.set_ylim(ymin=0)
# ax.xaxis.set_major_locator(plt.dates.YearLocator())
# ax.xaxis.set_major_formatter(plt.dates.DateFormatter('%Y'))
plt.legend()
# ax.xaxis.set_major_formatter(plt.dates.DateFormatter("%Y"))
fig.savefig(OUT_DIR + "tests-deleted-per-year.png", dpi=800)
# plt.show()
