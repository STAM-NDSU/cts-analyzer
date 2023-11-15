"""
Generate bargraphs for deleted tests and test deletion commits patterns [rq2]
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

plt.rcParams.update({"font.size": 6.5})

OUT_DIR = "../io/rq2/figures/"
# data = {
#     "commons-lang": {
#         "abc": 546,
#         "bcd": 688,
#         "cde": 67,
#         "def": 38,
#     },
#     "gson": {
#         "abc": 197,
#         "bcd": 226,
#         "cde": 26,
#         "def": 23,
#     },
#     "commons-math": {
#         "abc": 2090,
#         "bcd": 2738,
#         "cde": 163,
#         "def": 105,
#     },
#     "jfreechart": {
#         "abc": 98,
#         "bcd": 122,
#         "cde": 11,
#         "def": 9,
#     },
#     "joda-time": {
#         "abc": 191,
#         "bcd": 291,
#         "cde": 26,
#         "def": 7,
#     },
#     "pmd": {
#         "abc": 89,
#         "bcd": 1548,
#         "cde": 163,
#         "def": 37,
#     },
#     "cts": {
#         "abc": 0,
#         "bcd": 14723,
#         "cde": 673,
#         "def": 427,
#     },
# }

# result = {"projects": [], "abc": [], "bcd": [], "cde": [], "def": []}
# for key, value in data.items():
#     result["projects"].append(key)
#     result["abc"].append(value["abc"])
#     result["bcd"].append(value["bcd"])
#     result["cde"].append(value["cde"])
#     result["def"].append(value["def"])
# print(result)

df = {
    "projects": [
        "commons-lang",
        "gson",
        "commons-math",
        "jfreechart",
        "joda-time",
        "pmd",
        "cts",
    ],
    "abc": [546, 197, 2090, 98, 191, 89, 0],
    "~abc": [546, 197, 2090, 98, 191, 89, 0],
}

# # sns.barplot(df, x="projects", y="abc", legend=True)
# # plot bars in stack manner
# sns.barplot(df, x="projects", y="abc", color="r")
# sns.barplot(df, x="projects", y="bcd", bottom=df["abc"], color="b")
# sns.barplot(df, x="projects", y="cde", bottom=df["abc"] + df["bcd"], color="y")
# sns.barplot(
#     df, x="projects", y="def", bottom=df["abc"] + df["bcd"] + df["cde"], color="g"
# )
# sns.xlabel("Teams")
# sns.ylabel("Score")


df_rq21 = {
    "projects": [
        "commons-lang",
        "gson",
        "commons-math",
        "jfreechart",
        "joda-time",
        "pmd",
    ],
    "abc": [546, 197, 2090, 98, 191, 89],
    "~abc": [323, 63, 1226, 53, 469, 1173],
}
fig, ax = plt.subplots(figsize=(4, 2))
df_rq21 = pd.DataFrame(df_rq21)
df_rq21.plot(
    x="projects",
    kind="barh",
    stacked=True,
    color={"abc": "orange", "~abc": "green"},
    width=0.4,
    ax=ax
    # title="Stacked Bar Graph by dataframe"
)
plt.xlabel("Total Deleted Tests")
plt.ylabel("Projects")
ax.legend(["Deleted with API methods", "Deleted Without API Methods"])


# function to add value labels
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha="center")


# addlabels(df_rq21["projects"], df_rq21["abc"])
plt.gcf().subplots_adjust(left=0.25, bottom=0.2)
fig.savefig(OUT_DIR + "deleted_with_source_code.png", dpi=800)
plt.show()
