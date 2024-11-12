"""
Compute Coverage Loss stat which includes branch convergae loss and line coverage loss calculated using JaCoCo plugin. Futhermore, it also computes
Mutation Detection Loss computed using PIT plugin. 
"""

import pandas as pd
import math
from statistics import median

PROJECT_DIR = "../io/validationFiles/not-obsolete-coverage"
projects_list = [
    "commons-lang",
    "commons-math",
    "joda-time",
    "pmd",
]
SCALAR = 10000


# Varibles for box plot
all_projects_mutation_score = []
all_projects_line_coverage = []
all_projects_branch_coverage = []


def compute_deleted_tests_coverage_stats(project):
    print("########## Deleted Tests Coverage Stats ##########")
    file_path = PROJECT_DIR + "/deleted-tests/" + project + ".csv"
    _compute(file_path)


def _compute(file_path):
    # Process file
    original_df = pd.read_csv(file_path, thousands=",")
    original_df = original_df[original_df["Test Run"] == "passed"]
    print("Total Records: ", original_df.shape[0])
    print("Total Unique Parent Records: ", len(set(original_df["Parent"].to_list())))
    ## DEBUG
    # print(original_df.columns)

    ##### Calculate JACOCO: Branch and Line Coverage ######

    # Display 'Test Run' by group summary
    # print(df['Test Run'].value_counts().to_dict())

    # Parse types for the passed df
    df = original_df[original_df["Test Run"] == "passed"]
    df = df.astype(
        {
            "BC Before Covered": int,
            "BC Before Total": int,
            "BC After Covered": int,
            "BC After Total": int,
            "LC Before Covered": int,
            "LC Before Total": int,
            "LC After Covered": int,
            "LC After Total": int,
        }
    )

    df["BC Before Cov %"] = round(
        (df["BC Before Covered"] / df["BC Before Total"]) * 100 * SCALAR
    )
    df["BC After Cov %"] = round(
        (df["BC After Covered"] / df["BC After Total"]) * 100 * SCALAR
    )
    df["BC Loss %"] = df["BC Before Cov %"] - df["BC After Cov %"]

    df["LC Before Cov %"] = round(
        (df["LC Before Covered"] / df["LC Before Total"]) * 100 * SCALAR
    )
    df["LC After Cov %"] = round(
        (df["LC After Covered"] / df["LC After Total"]) * 100 * SCALAR
    )
    df["LC Loss %"] = df["LC Before Cov %"] - df["LC After Cov %"]

    df = df.astype(
        {
            "LC Loss %": int,
            "BC Loss %": int,
        }
    )

    ####### Prepare data for FAST-R  #######
    # WARNING: DO NOT MODIFY `df`
    copy_df = df.copy()
    # Commen out as we want to consider all the tests including coverage reducing tests
    # copy_df = copy_df[copy_df["LC Before Covered"] == copy_df["LC After Covered"]] 
    copy_df.to_csv("./fast-r/" + project + ".csv")
    ####### Prepare data for FAST-R  #######

    # Branch Coverage Changes
    branch_coverage_change_mask = df["BC Before Covered"] != df["BC After Covered"]
    branch_coverage_change_df = df[branch_coverage_change_mask]

    # Accumulate Branch Coverage Change

    all_projects_branch_coverage.extend(
        branch_coverage_change_df["BC Loss %"].tolist()
    )  # Box Plot

    # Print BC stats
    print(
        f"Total Records with Branch Coverage Change: {branch_coverage_change_df.shape[0]}"
    )
    print(
        f"Total Unique Parent Records: {len(set(branch_coverage_change_df['Parent'].to_list()))}"
    )
    print(
        f"Max Branch Coverage Change: {branch_coverage_change_df['BC Loss %'].max()/SCALAR:.4f}%"
    )
    print(
        f"Min Branch Coverage Change: {branch_coverage_change_df['BC Loss %'].min()/SCALAR:.4f}%"
    )

    # Line Coverage Changes
    line_coverage_change_mask = df["LC Before Covered"] != df["LC After Covered"]
    line_coverage_change_df = df[line_coverage_change_mask]

    # Accumulate Line Coverage Change
    all_projects_line_coverage.extend(
        line_coverage_change_df["LC Loss %"].dropna().tolist()
    )  # Box Plot

    # Print LC stats
    print(
        f"Total Records with Line Coverage Change: {line_coverage_change_df.shape[0]}"
    )
    print(
        f"Total Unique Parent Records: {len(set(line_coverage_change_df['Parent'].to_list()))}"
    )
    print(
        f"Max Line Coverage Change: {branch_coverage_change_df['LC Loss %'].dropna().max()/SCALAR:.4f}%"
    )
    print(
        f"Min Line Coverage Change: {branch_coverage_change_df['LC Loss %'].dropna().min()/SCALAR:.4f}%"
    )

    ##### Calculate PIT: Mutation Coverage ######
    # Failed
    failed_df = original_df[original_df["Mutation Run"] == "failed"]
    print(f"Mutation Total Fail: {failed_df.shape[0]}")
    print(
        f"Mutation Total Fail Unique Parent Records: {len(set(failed_df['Parent'].to_list()))}"
    )

    # Passed
    passed_df = original_df[original_df["Mutation Run"] == "passed"]
    print(f"Mutation Total Passs: {passed_df.shape[0]}")
    print(
        f"Mutation Total Passs Unique Parent Records: {len(set(passed_df['Parent'].to_list()))}"
    )

    # Parse types for the passed df
    passed_df = passed_df.astype(
        {
            "MC Before Killed": int,
            "MC Before Total": int,
            "MC After Killed": int,
            "MC After Total": int,
        }
    )

    passed_df["MC Before Cov %"] = round(
        (passed_df["MC Before Killed"] / passed_df["MC Before Total"]) * 100 * SCALAR, 0
    )
    passed_df["MC After Cov %"] = round(
        (passed_df["MC After Killed"] / passed_df["MC After Total"]) * 100 * SCALAR, 0
    )
    passed_df["MC Loss %"] = passed_df["MC Before Cov %"] - passed_df["MC After Cov %"]
    passed_df = passed_df.astype(
        {
            "MC Loss %": int,
        }
    )

    # Mutation Coverage Changes
    mutation_score_change_mask = (
        passed_df["MC Before Killed"] != passed_df["MC After Killed"]
    )
    mutation_coverage_change_df = passed_df[mutation_score_change_mask]

    # Accumulate Mutation Coverage Change
    all_projects_mutation_score.extend(
        mutation_coverage_change_df["MC Loss %"].dropna().tolist()
    )  # Box Plot

    # Print MC stats
    print(
        f"Total Records with Mutation Coverage Change: {mutation_coverage_change_df.shape[0]}"
    )
    print(
        f"Total Unique Parent Records: {len(set(mutation_coverage_change_df['Parent'].to_list()))}"
    )
    print(
        f"Max Mutation Coverage Change: {mutation_coverage_change_df['MC Loss %'].max()/SCALAR:.4f}%"
    )
    print(
        f"Min Mutation Coverage Change: {mutation_coverage_change_df['MC Loss %'].min()/SCALAR:.4f}%"
    )


for project in projects_list:
    print(f"______________Project: {project}____________")
    compute_deleted_tests_coverage_stats(project)


################ Preprocess data for box plot in R ################
def preprocess_data_for_boxplot_R():
    all_data = []

    def filter_zeros(data):
        return list(filter(lambda x: x != 0, data))

    def append_item(loss, type):
        all_data.append(
            [
                type,
                loss,
            ]
        )

    def export_csv():

        all_projects_branch_coverage_data = filter_zeros(all_projects_branch_coverage)
        bc_data = []
        for data in all_projects_branch_coverage_data:
            # Round to whole number
            data = int(math.ceil(data / SCALAR))
            append_item(
                "BC Loss",
                data,
            )
            bc_data.append(data)

        print(
            "--------------------Preprocess data for box plot in R--------------------"
        )
        print(f"Branch Coverage:")
        print(f"Min: {min(bc_data)}")
        print(f"Median: {median(bc_data)}")
        print(f"Max: {max(bc_data)}")

        all_projects_line_coverage_data = filter_zeros(all_projects_line_coverage)
        lc_data = []
        for data in all_projects_line_coverage_data:
            # Round to whole number
            data = int(math.ceil(data / SCALAR))
            append_item(
                "LC Loss",
                data,
            )
            lc_data.append(data)
        print(f"Line Coverage:")
        print(f"Min: {min(lc_data)}")
        print(f"Median: {median(lc_data)}")
        print(f"Max: {max(lc_data)}")

        all_projects_mutation_score_data = filter_zeros(all_projects_mutation_score)
        mc_data = []
        for data in all_projects_mutation_score_data:
            # Round to 4th decimal
            data = round(data / SCALAR, 4)
            append_item("MS Loss", data)
            mc_data.append(data)

        print("Mutation Score")
        print(f"Min: {min(mc_data)}")
        print(f"Median: {median(mc_data)}")
        print(f"Max: {max(mc_data)}")
        print(
            "--------------------Preprocess data for box plot in R--------------------"
        )

        # Create the pandas DataFrame
        df = pd.DataFrame(
            all_data,
            columns=[
                "Loss",
                "Type",
            ],
        )
        df.to_csv("coverage_mutation_loss_data.csv", index=False)
        df.to_csv("~/Documents/coverage_mutation_loss_data.csv", index=False)

    export_csv()


preprocess_data_for_boxplot_R()
################ Preprocess data for box plot in R ################
