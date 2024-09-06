"""
Generate pie chart for distribution of deleted tests by projects [rq2]

Use the chart without percentages, but make the following modifications:
Reduce the size of the circle/graph, maybe by 25-30%.
Put the number of tests outside the chart, maybe in a bracket after or below the project name.
Increase the font size of the labels/project names and numbers.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.rcParams.update({"font.size": 10})

# Data
deleted_tests = [260, 3316,  869,   660, 2070, 151, 17105]
labels = [
    "gson (260)",
    "commons-math (3,316)",
    "commons-lang (869)",
    "joda-time (660)",
    "pmd (2,070)",
    "jfreechart (151)",
    "cts (17105)",
]

# Set a custom color palette for a more sophisticated look
colors = sns.color_palette("deep")


# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(4, 4))
# plt.pie(deleted_tests, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 12})

def func(pct, allvals):
    absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
    return f"{absolute:d}"


plt.pie(
    deleted_tests,
    labels=labels,
    # autopct=lambda pct: func(pct, deleted_tests),
    # pctdistance=0.75,
    startangle=275,
    colors=colors,
    textprops={"fontsize": 10},
)

# # Draw a circle in the center to make it look like a donut chart
# centre_circle = plt.Circle((0,0),0.70,fc='white')
# fig = plt.gcf()
# fig.gca().add_artist(centre_circle)

# Set title and legend
# plt.title('Distribution of Deleted Tests for Each Library', fontsize=12)
# plt.legend(labels, loc='upper right', bbox_to_anchor=(1.2, 1))

# Show the plot
# plt.show()
# plt.gcf().subplots_adjust(left=0, bottom=0, top=0.7, right=1, hspace=0, wspace=0)

# plt.gcf().subplots_adjust(bottom=0.5)
plt.margins(0,0)
fig.tight_layout()
# plt.gca().spines[['right', 'top']].set_visible(False)

OUT_DIR = "../io/rq2/figures/"
plt.savefig(OUT_DIR + "deleted_tests_by_projects02.pdf", dpi=1200,  bbox_inches="tight", pad_inches=0,)
plt.savefig(OUT_DIR + "deleted_tests_by_projects02.png", dpi=1200, bbox_inches="tight", pad_inches=0,)
