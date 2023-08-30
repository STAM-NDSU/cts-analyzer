"""
Generate box plot for commits between test deletion commit [rq1]
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
projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

OUT_DIR = "../io/rq1/figures/days_commits/boxplots/"
IO_DIR = "../io/validationFiles"
COMMIT_COLOR = "red"

plt.rcParams.update({'font.size': 6})

for p_index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        test_deletion_datetime_inbetweencommits_range_file_path = Path(
            f"{IO_DIR}/{project}/test_deletion_datetime_inbetweencommits_range.csv"
        )

        if not os.path.exists(
            f"{test_deletion_datetime_inbetweencommits_range_file_path}"
        ):
            print(
                "Error: path does not exit -> ",
                test_deletion_datetime_inbetweencommits_range_file_path,
            )

        
        df = pd.read_csv(test_deletion_datetime_inbetweencommits_range_file_path)
        df = df.loc[1:, :]
        types_dict = {"Range": int}
        for col, col_type in types_dict.items():
            df[col] = df[col].astype(col_type)

        fig, ax1 = plt.subplots(figsize=(1, 0.75))
        bp1 = ax1.violinplot(
            df["Commits"], positions=[0.5], showmeans=False, showmedians=False, showextrema=False, vert = False
        )
        
        ax1.boxplot(df["Commits"], positions=[0.5], showfliers=False, vert = False)
        # ax1.set_xlabel("Commits", color=COMMIT_COLOR, fontsize=10)
        # ax1.xaxis.grid(True)
        # ax1.set_xlim(0, 2)
        ax1.set_ylim(0)
        ax1.set_xlim(0)
        ax1.tick_params(axis="x", labelcolor="#000000", labeltop=True, top=True, labelbottom=False, bottom=False)
     

        print(bp1.keys())
        plt.setp(bp1["bodies"], color=COMMIT_COLOR,)
        # plt.setp(bp1["whiskers"], color=COMMIT_COLOR,)
        # plt.setp(bp1["caps"], color=COMMIT_COLOR,)
        # plt.setp(bp1["fliers"], color=COMMIT_COLOR,)

        # set visibility of x-axis as False
        xax = ax1.axes.get_xaxis()
        xax = xax.set_visible(True)
        
        # set visibility of y-axis as False
        yax = ax1.axes.get_yaxis()
        yax = yax.set_visible(False)
        
        # set visibility of spines(border-box) as False
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(True)
        ax1.spines['left'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        
        fig.savefig(
            OUT_DIR + project + "_commits.png",
        )
        # plt.show()

    main(project)
