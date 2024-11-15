"""
Generate two y-axis line chart for version and year [rq1]
"""
import os.path
from pathlib import Path
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from collections import defaultdict
from matplotlib.gridspec import GridSpec


# explictit function to hide index
# of subplots in the figure
def formatAxes(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        ax.tick_params(labelbottom=False, labelleft=False)
 
 
plt.rcParams["figure.autolayout"] = True
OUT_DIR = "../io/rq1/figures/version_year/"

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    # "jfreechart",
    # "joda-time",
    # "pmd",
    # "cts",
]
alphabets = ["a", "b", "c", "d", "e", "f", "g"]
IO_DIR = "../io/validationFiles"
VERSION_COLOR = "red"
YEAR_COLOR = "green"


fig = plt.figure(constrained_layout=True)
gs = GridSpec(6, 2, figure=fig)

for p_index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        test_deletion_grouped_year_file_path = Path(
            f"{IO_DIR}/{project}/stat_test_deletion_commits_grouped_year.csv"
        )
        test_deletion_version_file_path = Path(
            f"{IO_DIR}/{project}/stat_version_test_deletion.csv"
        )

        if not os.path.exists(f"{test_deletion_grouped_year_file_path}"):
            print("Error: path does not exit -> ", test_deletion_grouped_year_file_path)
        if not os.path.exists(f"{test_deletion_version_file_path}"):
            print("Error: path does not exit -> ", test_deletion_version_file_path)

        figsize = (6, 8)
        titlepos = -0.12
        if project == "jfreechart":
            figsize = (6, 3)
            titlepos = -0.28
        elif project == "gson":
            figsize = (6, 5)
            titlepos = -0.19
        elif project == "joda-time":
            figsize = (6, 5)
            titlepos = -0.19
        elif project == "pmd":
            figsize = (6, 10)
            titlepos = -0.08
        # fig, ax1 = plt.subplots(figsize=figsize)
        # ax1.tick_params(axis="x")


        # create sub plots as grid
        if project =="commons-lang":
            ax1 = fig.add_subplot(gs[0:2, 0])
        elif project == "gson":
            ax1 = fig.add_subplot(gs[1, 1])
        elif project == "commons-math":
            ax1 = fig.add_subplot(gs[0:2, 1])
        elif project == "joda-time":
            ax1 = fig.add_subplot(gs[2, 1])
        elif project == "jfreechart":
            ax1 = fig.add_subplot(gs[3, 1])
        elif project == "pmd":
            ax1 = fig.add_subplot(gs[1:, 0])
        elif project == "cts":
            ax1 = fig.add_subplot(gs[5:, :])

        # Handle axis 1
        version_df = pd.read_csv(test_deletion_version_file_path, dtype=str)
        types_dict = {"Total Deleted Tests": int, "Test Deletion Commits": int}
        for col, col_type in types_dict.items():
            version_df[col] = version_df[col].astype(col_type)
        print(version_df.dtypes)
        verfion_deleted_df = version_df[version_df["Total Deleted Tests"] > 0]
        marker = None
        linestyle = "dashed"
        lw = 1
        if project == "jfreechart":
            marker = "o"
        ax1.plot(
            verfion_deleted_df["Total Deleted Tests"],
            verfion_deleted_df["Tag"],
            color=VERSION_COLOR,
            lw=lw,
            linestyle=linestyle,
            label="tests",
            marker=marker,
        )
        marker = None
        linestyle = "solid"
        lw = 1
        if project == "jfreechart":
            marker = "x"
        ax1.plot(
            verfion_deleted_df["Test Deletion Commits"],
            verfion_deleted_df["Tag"],
            color=VERSION_COLOR,
            lw=lw,
            linestyle=linestyle,
            label="commits",
            marker=marker,
        )
        ax1.set_ylabel("Version", color=VERSION_COLOR, fontsize=12)
        ax1.legend(loc="upper left")
        ax1.tick_params(axis="y", labelcolor=VERSION_COLOR)
        ax1.set_xlabel("Num. of commits and tests", fontsize=12)
        # Handle axis 2
        year_df = pd.read_csv(test_deletion_grouped_year_file_path, dtype=str)
        types_dict = {"Testcase": int, "Commit": int}
        for col, col_type in types_dict.items():
            year_df[col] = year_df[col].astype(col_type)

        ax2 = ax1.twinx()
        ax2.plot(
            year_df["Testcase"],
            year_df["Datetime"],
            color=YEAR_COLOR,
            lw=1,
            linestyle="dashed",
            label="tests",
        )
        ax2.plot(
            year_df["Commit"],
            year_df["Datetime"],
            color=YEAR_COLOR,
            lw=1,
            linestyle="solid",
            label="commits",
        )
        ax2.set_ylabel("Year", color=YEAR_COLOR, fontsize=12)
        ax2.legend(loc="upper right")
        ax2.tick_params(axis="y", labelcolor=YEAR_COLOR)

        # two_year_locator = mdates.MonthLocator(interval=48)
        # year_month_formatter = mdates.DateFormatter("%Y") # four digits for year, two for month
        # ax2.yaxis.set_major_locator(two_year_locator)
        # ax2.yaxis.set_major_formatter(year_month_formatter) # formatter for major axis only

        # plt.text(120, -2.25, "(" + alphabets[p_index] + ") " + project, fontsize=12)
        plt.title("(" + alphabets[p_index] + ") " + project, y=titlepos)
        # fig.autofmt_xdate()

        # fig.tight_layout()
        # fig.savefig(
        #     OUT_DIR + project + "_tests_by_version_year.png",
        # )
        # plt.show()

    main(project)


# formatAxes(fig)
plt.show()