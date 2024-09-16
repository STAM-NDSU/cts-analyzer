import pandas as pd
import glob


PROJECT_DIR = "../io/validationFiles/not-obsolete-coverage"
projects_list = [
    # "commons-lang",
    # "gson",
    # "commons-math",
    # "jfreechart",
    # "joda-time",
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
    
    ##### Calculate JACOCO: Branch and Line Coverage ######
        
    # Initialize counters and accumulators
    total_failed = 0
    total_passed = 0
    total_commits_with_branch_coverage_change = 0
    total_tests_with_branch_coverage_change = 0
    total_commits_with_line_coverage_change = 0
    total_tests_with_line_coverage_change = 0

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
    total_commits_with_branch_coverage_change += (
        df[branch_coverage_change_mask].drop_duplicates(subset=["Hash"]).shape[0]
    )
    total_tests_with_branch_coverage_change = df[branch_coverage_change_mask].shape[0]

    # Line Coverage Changes
    line_coverage_change_mask = df["LC Before Covered"] != df["LC After Covered"]
    total_commits_with_line_coverage_change = (
        df[line_coverage_change_mask].drop_duplicates(subset=["Hash"]).shape[0]
    )
    total_tests_with_line_coverage_change = df[line_coverage_change_mask].shape[0]

    # Calculate Line Coverage Change
    line_coverage_changes.extend(
        (df["LC Before Cov %"] - df["LC After Cov %"]).dropna().tolist()
    )
    # Filter zeros from list
    line_coverage_changes = list(filter(lambda x: x != 0, line_coverage_changes))
    print(line_coverage_changes)

    # Calculate Branch Coverage Change
    branch_coverage_changes.extend(
        (df["BC Before Cov %"] - df["BC After Cov %"]).dropna().tolist()
    )
    # Filter zeros from list
    branch_coverage_changes = list(filter(lambda x: x != 0, branch_coverage_changes))
    print(branch_coverage_changes)

    # Average, Max, and Min Line Coverage Change
    avg_line_coverage_change = (
        sum(line_coverage_changes) / len(line_coverage_changes)
        if line_coverage_changes
        else 0
    )
    max_line_coverage_change = max(line_coverage_changes, default=0)
    min_line_coverage_change = min(line_coverage_changes, default=0)

    ## DEBUG
    # print("Max line coverage is:")
    # max_line_coverage_index = line_coverage_changes.index(max_line_coverage_change)
    # print(df.loc[max_line_coverage_index, :])

    # Average, Max, and Min Branch Coverage Change
    avg_branch_coverage_change = (
        sum(branch_coverage_changes) / len(branch_coverage_changes)
        if branch_coverage_changes
        else 0
    )
    max_branch_coverage_change = max(branch_coverage_changes, default=0)
    min_branch_coverage_change = min(branch_coverage_changes, default=0)

    # DEBUG
    print("Max branch coverage is:")
    max_branch_coverage_index = branch_coverage_changes.index(
        max_branch_coverage_change
    )
    print(df.loc[max_branch_coverage_index, :])

    # Print results
    print(f"Total Failed: {total_failed}")
    print(f"Total Passed: {total_passed}")
    print(
        f"Total Commits with Branch Coverage Change: {total_commits_with_branch_coverage_change}"
    )
    print(
        f"Total Tests with Branch Coverage Change: {total_tests_with_branch_coverage_change}"
    )
    print(
        f"Total Commits with Line Coverage Change: {total_commits_with_line_coverage_change}"
    )
    print(
        f"Total Tests with Line Coverage Change: {total_tests_with_line_coverage_change}"
    )
    print(f"Avg Line Coverage Change: {avg_line_coverage_change/SCALAR:.4f}%")
    print(f"Max Line Coverage Change: {max_line_coverage_change/SCALAR:.4f}%")
    print(f"Min Line Coverage Change: {min_line_coverage_change/SCALAR:.4f}%")
    print(f"Avg Branch Coverage Change: {avg_branch_coverage_change/SCALAR:.4f}%")
    print(f"Max Branch Coverage Change: {max_branch_coverage_change/SCALAR:.4f}%")
    print(f"Min Branch Coverage Change: {min_branch_coverage_change/SCALAR:.4f}%")

    ##### Calculate PMD: Mutation Coverage ######
    
    # Initialize counters and accumulators
    total_failed = 0
    total_passed = 0
    total_commits_with_mutation_coverage_change = 0
    total_tests_with_mutation_coverage_change = 0
    
    mutation_coverage_changes = []

    # Total Failed
    total_failed = original_df[original_df["Mutation Run"] == "failed"].shape[0]

    # Total Passed
    total_passed = df.shape[0] - total_failed

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
    total_commits_with_mutation_coverage_change = (
        df[mutation_coverage_change_mask].drop_duplicates(subset=["Hash"]).shape[0]
    )
    total_tests_with_mutation_coverage_change = df[mutation_coverage_change_mask].shape[
        0
    ]

    # Calculate Mutation Coverage Change
    mutation_coverage_changes.extend(
        (df["MC Before Cov %"] - df["MC After Cov %"]).dropna().tolist()
    )

    # Average, Max, and Min Mutation Coverage Change
    avg_mutation_coverage_change = (
        sum(mutation_coverage_changes) / len(mutation_coverage_changes)
        if mutation_coverage_changes
        else 0
    )
    max_mutation_coverage_change = max(mutation_coverage_changes, default=0)
    min_mutation_coverage_change = min(mutation_coverage_changes, default=0)

    print(
        f"Total Commits with Mutation Coverage Change: {total_commits_with_mutation_coverage_change}"
    )
    print(
        f"Total Tests with Mutation Coverage Change: {total_tests_with_mutation_coverage_change}"
    )
    print(f"Avg Mutation Coverage Change: {avg_mutation_coverage_change/SCALAR:.4f}%")
    print(f"Max Mutation Coverage Change: {max_mutation_coverage_change/SCALAR:.4f}%")
    print(f"Min Mutation Coverage Change: {min_mutation_coverage_change/SCALAR:.4f}%")


for project in projects_list:
    print("Project:", project)
    compute_parent_test_deletion_commits_coverage_stats(project)
    # compute_deleted_tests_coverage_stats(project)


# ########## Parent TDC Coverage Stats ##########
# {"['32a76bd602fcdb947bbca3465403c6ee7430ec89']", "['']", "['']", "['']", "['a5d9de59f8b966b0c1599432b0252984c4e597a0']", "['16a4aa3163061011b08564c5bda50db543e3f6e9']", "['2ec77ad02fde8ceb56eed684b3ba34b7510ea9f8']", "['d650c87d8d4a60d4ad6fe2a514524d952a50bd94']", "['1f2aa739b4988e9932eb582b16a773061a1884ff']", "['5485794da51bfbe2f4ed039ade630eb4b4a26f90']", "['c66b3e8fa9f875cb63c25a12e88ae88b898e10a7']", "['de709946757119a428e240bfeaab422c138b7d18']", "['1d7f9641262b97bd38c2be9742120b937d6c2f87']", "['134dbed07e8fb20bc01e3543803ca72a065187da', '70079f0842ed16d92ccaf6234104da5c6c791590']", "['094ce26227e7f064dc7b462ce952b41f3bc8cf5e']"}
# ########## Deleted Tests Coverage Stats ##########
# {'', '', '2ec77ad02fde8ceb56eed684b3ba34b7510ea9f8', 'c66b3e8fa9f875cb63c25a12e88ae88b898e10a7', 'a5d9de59f8b966b0c1599432b0252984c4e597a0', '1f2aa739b4988e9932eb582b16a773061a1884ff', '16a4aa3163061011b08564c5bda50db543e3f6e9', '134dbed07e8fb20bc01e3543803ca72a065187da', '094ce26227e7f064dc7b462ce952b41f3bc8cf5e', '', 'd650c87d8d4a60d4ad6fe2a514524d952a50bd94'}
