"""
Generate box plot for num. of test deletion commits & deleted tests in version [rq1]
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
import seaborn as sns

plt.rcParams["figure.autolayout"] = True
OUT_DIR = "../io/rq1/figures/version_year/"

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]
alphabets = ["a", "b", "c", "d", "e", "f", "g"]
IO_DIR = "../io/validationFiles"
COMMIT_COLOR = "red"
DAYS_COLOR = "green"

medians = []
test_deletion_commits_timerange = {}
for p_index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        test_deletion_version_file_path = Path(
            f"{IO_DIR}/{project}/stat_version_test_deletion.csv"
        )

        if not os.path.exists(f"{test_deletion_version_file_path}"):
            print(
                "Error: path does not exit -> ",
                test_deletion_version_file_path,
            )

        # In [23]: df[[0, 1, 2, 3]].plot(kind='box', ax=ax)
        # Out[23]: <matplotlib.axes._subplots.AxesSubplot at 0x4890978>
        # In [24]: ax2 = ax.twinx()
        # In [25]: ax2.boxplot(df[4], positions=[4])
        # In [27]: ax.set_xlim(0, 5)
        # Out[27]: (0, 5)

        fig, ax1 = plt.subplots(figsize=(3, 3))
        ax1.tick_params(axis="x")

        # Handle axis 1
        df = pd.read_csv(test_deletion_version_file_path)
        df = df.loc[1:, :]
        types_dict = {"Test Deletion Commits": int, "Total Deleted Tests": int}
        for col, col_type in types_dict.items():
            df[col] = df[col].astype(col_type)
        print(df.dtypes)

        # df["Test Deletion Commits"].plot(kind='box', ax=ax1)
        bp1 = ax1.violinplot(
            df["Test Deletion Commits"],
            positions=[0.5],
            showmeans=False,
            showmedians=False,
            showextrema=False,
        )
        ax1.set_ylabel("Commits", color=COMMIT_COLOR, fontsize=10)
        ax1.tick_params(axis="y", labelcolor=COMMIT_COLOR)
        ax1.boxplot(df["Test Deletion Commits"], positions=[0.5], showfliers=False)
        # ax1.yaxis.grid(True)
        ax1.set_xlim(0, 2)
        # ax1.set_ylim(0)
        ax1.tick_params(labelbottom=False, bottom=False)
        # ax1.set_xticks([1,2],label=['',''])
        # ax1.set(xlabel=None)

        print(bp1.keys())
        plt.setp(
            bp1["bodies"],
            color=COMMIT_COLOR,
        )
        # plt.setp(bp1["whiskers"], color=COMMIT_COLOR,)
        # plt.setp(bp1["caps"], color=COMMIT_COLOR,)
        # plt.setp(bp1["fliers"], color=COMMIT_COLOR,)

        # Handle axis 2
        ax2 = ax1.twinx()
        bp2 = ax2.violinplot(
            df["Total Deleted Tests"],
            positions=[1.5],
            showmeans=False,
            showmedians=False,
            showextrema=False,
        )
        ax2.boxplot(df["Total Deleted Tests"], positions=[1.5], showfliers=False)
        ax2.set_ylabel("Tests", color=DAYS_COLOR, fontsize=10)
        ax2.tick_params(axis="y", labelcolor=DAYS_COLOR)
        # ax2.set_ylim(0)
        plt.setp(
            bp2["bodies"],
            color=DAYS_COLOR,
        )
        # plt.setp(bp2["whiskers"], color=DAYS_COLOR,)
        # plt.setp(bp2["fliers"], color=COMMIT_COLOR,)
        # fig.tight_layout()

        plt.title("(" + alphabets[p_index] + ") " + project, y=-0.19, fontsize=10)
        fig.savefig(
            OUT_DIR + project + "_boxplot_version.png",
        )
        plt.show()

    main(project)
