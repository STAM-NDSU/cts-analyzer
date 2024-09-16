"""
Compute Coverage Loss stat which includes branch convergae loss and line coverage loss calculated using JaCoCo plugin. Futhermore, it also computes
Mutation Detection Loss computed using PIT plugin. 
"""

import pandas as pd


PROJECT_DIR = "../io/validationFiles/not-obsolete-coverage"
projects_list = [
    "commons-lang",
    # "gson",
    "commons-math",
    # "jfreechart",
    "joda-time",
    "pmd",
]
SCALAR = 10000


def compute_parent_test_deletion_commits_coverage_stats(project):
    print("########## Parent TDC Coverage Stats ##########")
    file_path = PROJECT_DIR + "/parent-test-deletion-commits/" + project + ".csv"
    _compute(file_path)


def compute_deleted_tests_coverage_stats(project):
    print("########## Deleted Tests Coverage Stats ##########")
    file_path = PROJECT_DIR + "/deleted-tests/" + project + ".csv"
    _compute(file_path)


def _compute(file_path):
    # Process file
    original_df = pd.read_csv(file_path, thousands=",")
    ## DEBUG
    # print(original_df.columns)

    ##### Calculate JACOCO: Branch and Line Coverage ######

    # Initialize counters and accumulators
    total_failed = 0
    total_passed = 0
    total_records_with_branch_coverage_change = 0
    total_records_with_line_coverage_change = 0

    line_coverage_changes = []
    branch_coverage_changes = []

    # Display 'Test Run' by group summary
    # print(df['Test Run'].value_counts().to_dict())

    # Total Failed
    total_failed = original_df[original_df["Test Run"] == "failed"].shape[0]

    # Total Passed
    total_passed = original_df.shape[0] - total_failed

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
        (df["BC Before Covered"] / df["BC Before Total"]) * SCALAR, 0
    )
    df["BC After Cov %"] = round(
        (df["BC After Covered"] / df["BC After Total"]) * SCALAR, 0
    )
    df["LC Before Cov %"] = round(
        (df["LC Before Covered"] / df["LC Before Total"]) * SCALAR, 0
    )
    df["LC After Cov %"] = round(
        (df["LC After Covered"] / df["LC After Total"]) * SCALAR, 0
    )
    df = df.astype(
        {
            "BC Before Cov %": int,
            "BC After Cov %": int,
            "LC After Cov %": int,
            "LC Before Cov %": int,
        }
    )

    # # DEBUG
    # branch_coverage_faulty_mask = df["BC Before Cov %"] > df["BC After Cov %"]
    # df = df[branch_coverage_faulty_mask]
    # print(set(df['Hash'].to_list()))

    # Branch Coverage Changes
    branch_coverage_change_mask = df["BC Before Covered"] != df["BC After Covered"]
    total_records_with_branch_coverage_change = df[branch_coverage_change_mask].shape[0]

    # Line Coverage Changes
    line_coverage_change_mask = df["LC Before Covered"] != df["LC After Covered"]
    total_records_with_line_coverage_change = df[line_coverage_change_mask].shape[0]

    # Calculate Line Coverage Change
    line_coverage_changes.extend(
        (df["LC Before Cov %"] - df["LC After Cov %"]).dropna().tolist()
    )
    # Filter zeros from list; Helpful to calculate avg change
    # line_coverage_changes = list(filter(lambda x: x != 0, line_coverage_changes))
    # print(line_coverage_changes)

    # Calculate Branch Coverage Change
    branch_coverage_changes.extend(
        (df["BC Before Cov %"] - df["BC After Cov %"]).dropna().tolist()
    )
    # # Filter zeros from list; Helpful to calculate avg change
    # branch_coverage_changes = list(filter(lambda x: x != 0, branch_coverage_changes))
    # print(branch_coverage_changes)

    # Max Line Coverage Change
    max_line_coverage_change = max(line_coverage_changes, default=0)

    # DEBUG
    # print("Max line coverage is:")
    # max_line_coverage_index = line_coverage_changes.index(max_line_coverage_change)
    # print(df.loc[max_line_coverage_index, :])

    # Max Branch Coverage Change
    max_branch_coverage_change = max(branch_coverage_changes, default=0)

    # DEBUG
    # print("Max branch coverage is:")
    # max_branch_coverage_index = branch_coverage_changes.index(
    #     max_branch_coverage_change
    # )
    # print(df.loc[max_branch_coverage_index, :])

    # Print results
    print(f"Total Failed: {total_failed}")
    print(f"Total Passed: {total_passed}")
    print(
        f"Total Records with Branch Coverage Change: {total_records_with_branch_coverage_change}"
    )
    print(
        f"Total Records with Line Coverage Change: {total_records_with_line_coverage_change}"
    )
    print(f"Max Line Coverage Change: {max_line_coverage_change/SCALAR:.4f}%")
    print(f"Max Branch Coverage Change: {max_branch_coverage_change/SCALAR:.4f}%")

    ##### Calculate PMD: Mutation Coverage ######

    # Initialize counters and accumulators
    total_failed = 0
    total_passed = 0
    total_records_with_mutation_coverage_change = 0

    mutation_coverage_changes = []

    # Total Failed
    total_failed = original_df[original_df["Mutation Run"] == "failed"].shape[0]

    # Total Passed
    total_passed = original_df.shape[0] - total_failed

    # Parse types for the passed df
    df = original_df[original_df["Mutation Run"] == "passed"]
    df = df.astype(
        {
            "MC Before Killed": int,
            "MC Before Total": int,
            "MC After Killed": int,
            "MC After Total": int,
        }
    )

    df["MC Before Cov %"] = round(
        (df["MC Before Killed"] / df["MC Before Total"]) * SCALAR, 0
    )
    df["MC After Cov %"] = round(
        (df["MC After Killed"] / df["MC After Total"]) * SCALAR, 0
    )

    df = df.astype({"MC Before Cov %": int, "MC After Cov %": int})

    # Mutation Coverage Changes
    mutation_coverage_change_mask = df["MC Before Killed"] != df["MC After Killed"]
    total_records_with_mutation_coverage_change = df[
        mutation_coverage_change_mask
    ].shape[0]

    # Calculate Mutation Coverage Change
    mutation_coverage_changes.extend(
        (df["MC Before Cov %"] - df["MC After Cov %"]).dropna().tolist()
    )

    # Max Mutation Coverage Change
    max_mutation_coverage_change = max(mutation_coverage_changes, default=0)

    print(f"Mutation Total Fail: {total_failed}")
    print(f"Mutation Total Passs: {total_passed}")
    print(
        f"Total Records with Mutation Coverage Change: {total_records_with_mutation_coverage_change}"
    )
    print(f"Max Mutation Coverage Change: {max_mutation_coverage_change/SCALAR:.4f}%")


for project in projects_list:
    print(f"______________Project: {project}____________")
    compute_parent_test_deletion_commits_coverage_stats(project)
    compute_deleted_tests_coverage_stats(project)
