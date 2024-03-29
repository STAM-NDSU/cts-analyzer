"""
Generate barchart for num. of deleted tests in year [rq1]
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
plt.rcParams.update({'font.size': 10})

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]
OUT_DIR = "../io/rq1/figures/version_year/bargraphs/"
IO_DIR = "../io/validationFiles"

for p_index, project in enumerate(projects_list):

    def main(project):
        print(project)
        print("-----------------")
        test_deletion_grouped_year_file_path = Path(
            f"{IO_DIR}/{project}/stat_test_deletion_commits_grouped_year.csv"
        )

        if not os.path.exists(f"{test_deletion_grouped_year_file_path}"):
            print(
                "Error: path does not exit -> ",
                test_deletion_grouped_year_file_path,
            )

        fig, ax1 = plt.subplots(figsize=(2,2))
        ax1.tick_params(axis="x")

        # Handle axis 1
        df = pd.read_csv(test_deletion_grouped_year_file_path)
        types_dict = {"Testcase": int, "Commit": int, "Datetime": str}
        for col, col_type in types_dict.items():
            df[col] = df[col].astype(col_type)
        print(df.dtypes)
        
        width = 0.8
        if project == "jfreechart":
            ax1.set_xlim(-0.88, 10)
        bp1 = ax1.bar(
            df["Datetime"],
            df["Commit"],
            width=width,
           
        )
        # getting current axes
        # a = plt.gca()
        
        # set visibility of x-axis as False
        xax = ax1.axes.get_xaxis()
        xax = xax.set_visible(False)
        
        # set visibility of y-axis as False
        yax = ax1.axes.get_yaxis()
        yax = yax.set_visible(True)
        
        # set visibility of spines(border-box) as False
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax1.spines['left'].set_visible(True)
        ax1.spines['bottom'].set_visible(False)
        
        # fig.tight_layout()
        fig.savefig(
            OUT_DIR + project + "_bargraph_year.png",
        )
        # plt.show()

    main(project)
