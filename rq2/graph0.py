"""
Generate pie chart for distribution of deleted tests by projects [rq2]
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.rcParams.update({"font.size": 8})

# Data
deleted_tests = [197, 2090, 546, 191, 897, 98, 1789]
labels = [
    "gson",
    "commons-math",
    "commons-lang",
    "joda-time",
    "pmd",
    "jfreechart",
    "cts",
]

# Set a custom color palette for a more sophisticated look
colors = sns.color_palette("deep")

# Create a pie chart with enhanced aesthetics
# fig, ax = plt.subplots(figsize=(3.5, 2))
plt.figure(figsize=(4, 3))
# plt.pie(deleted_tests, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 12})


def func(pct, allvals):
    absolute = int(np.round(pct / 100.0 * np.sum(allvals)))
    return f"{absolute:d}\n({pct:.1f}%)"


plt.pie(
    deleted_tests,
    labels=labels,
    autopct=lambda pct: func(pct, deleted_tests),
    startangle=90,
    colors=colors,
    textprops={"fontsize": 5},
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
plt.gcf().subplots_adjust(left=0, bottom=0, top=1, right=1, hspace=-0.2, wspace=0)
# plt.margins(0,0)

OUT_DIR = "../io/rq2/figures/"
plt.savefig(OUT_DIR + "deleted_with_source_code3.png", dpi=1200, bbox_inches="tight")
