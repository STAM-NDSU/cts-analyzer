from copy import deepcopy
from datetime import timedelta
from pydriller import Repository
import pandas as pd
from . import config
from .core import (
    analyze_test_cases_removal_in_commit_file,
    analyze_test_cases_addition_in_commit_file,
    analyze_true_test_cases_deletion_in_commit_file_javaparser,
    get_removed_test_functions_regex_only,
)
from .utils import (
    is_candidate_file,
    format_commit_datetime,
    get_full_commit_url,
    parse_commit_as_hyperlink,
    get_repo_name,
    strip_commit_url,
)

"""
  Analyze the target branch of the repository and get commits 
  that either remove tests cases and/or assertions
  from java test files that match the function definition regex 
"""


class AnalyzerGlobal:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(AnalyzerGlobal, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.since = config.COMMIT_START_Datetime
        self.to = config.COMMIT_END_Datetime
        self.commits = None
        self.current_commit = None
        self.results = []
        self.total_commits = 0
        self.total_test_removal_commits = 0
        self.total_high_conf_test_removal = 0
        self.total_low_conf_test_removal = 0
        self.step1_hydrated_df = None
        self.cloned_step1_hydrated_df = None
        self.step11_hydrated_df = None
        self.step2_hydrated_df = None
        self.cloned_step2_hydrated_df = None
        self.step3_hydrated_df = None

    @property
    def total_testcases(self):
        return len(self.results)

    def __repr__(self) -> str:
        return f"<since={self.since} to={self.to} commit={self.current_commit.hash}"


def get_removed_test_functions_details(
    repo_url, branch, step=None, previous_step_df=None
):
    def pretify_csv_results(analyzer_global):
        MIN_ROWS = 3
        MIN_COLUMNS = 9

        results = analyzer_global.results
        if len(results) < MIN_ROWS:
            fill_rows = MIN_ROWS - len(results)
            fill_columns = MIN_COLUMNS
            filled_rows = [[" "] * fill_columns for _ in range(0, fill_rows)]
            results = results + filled_rows
        results[0].insert(8, "Total Commits")
        results[0].insert(9, analyzer_global.total_commits)
        results[1].insert(8, "Total Testcases")
        results[1].insert(9, analyzer_global.total_testcases)

    def traverse_commits(analyzer_global):
        since = analyzer_global.since
        to = analyzer_global.to
        results = analyzer_global.results
        commits = Repository(
            repo_url,
            only_in_branch=branch,
            only_modifications_with_file_types=config.JAVA_FILE_EXT,
            since=since,
            to=to,
            only_no_merge=True,
            # single="14ec8c603243beccb580cfd12bb9d4dd4248e351",  # use it only for debugging
        ).traverse_commits()
        analyzer_global.commits = commits

        if not commits:
            print("No Commits---- Oopss")

        commits_to_look = []
        if step == 11:
            step1_hydrated_df = previous_step_df
            analyzer_global.cloned_step1_hydrated_df = step1_hydrated_df.copy(deep=True)
            print("Initial Dataframe: ", analyzer_global.cloned_step1_hydrated_df.shape)

            if step1_hydrated_df is not None:
                # WARNING: Previously, used to check for only commits with testcases not beginning with 'test';
                # cause of issue for showing private testcases
                # commits_to_look = step1_hydrated_df[
                #     step1_hydrated_df["Check Annot"] == "check"
                # ].to_dict("list")["Hash"]

                # Check for all the commits regardless of annotation check in step1
                commits_to_look = step1_hydrated_df.to_dict("list")["Hash"]
                commits_to_look = list(
                    set(list(map(lambda each: strip_commit_url(each), commits_to_look)))
                )
                print("Total commits to scan: ", len(commits_to_look))
        elif step == 3:
            step2_hydrated_df = previous_step_df
            analyzer_global.cloned_step2_hydrated_df = step2_hydrated_df.copy(deep=True)
            print("Initial Dataframe: ", analyzer_global.cloned_step2_hydrated_df.shape)

            if step2_hydrated_df is not None:
                commits_to_look = step2_hydrated_df.to_dict("list")["Hash"]
                commits_to_look = list(
                    set(list(map(lambda each: strip_commit_url(each), commits_to_look)))
                )
                print("Total commits to scan: ", len(commits_to_look))

        is_completed = False
        while not is_completed:
            commit = next(commits, None)
            if commit:
                commit_datetime = format_commit_datetime(commit.committer_date)
                commit_hash = parse_commit_as_hyperlink(
                    label=commit.hash, url=get_full_commit_url(commit.hash)
                )
                commit_msg = commit.msg
                
                
                # Handles step 1
                if step == 1:
                    analyzer_global.total_commits += 1
                    # Update current_commit pointer; to skip the corrupted ones
                    analyzer_global.current_commit = commit
                    analyzer_global.since = commit.committer_date
                    commit_master_data = [commit_datetime, commit_hash, commit_msg]

                    # Holds all test cases removed across multiple modified files;
                    all_removed_test_cases_in_commit = []

                    for file_idx, file in enumerate(commit.modified_files):
                        filename = file.filename
                        # Check if file is a candidate file
                        if not is_candidate_file(filename):
                            continue

                        all_removed_test_cases_file_data = (
                            analyze_test_cases_removal_in_commit_file(file)
                        )
                        all_removed_test_cases_file_data["file_index"] = file_idx
                        all_removed_test_cases_file_data["filename"] = filename
                        all_removed_test_cases_file_data["filepath"] = file.old_path
                        all_removed_test_cases_in_commit.append(
                            all_removed_test_cases_file_data
                        )

                    # Fully hydrate test cases records
                    for (
                        removed_test_cases_in_file_data
                    ) in all_removed_test_cases_in_commit:
                        removed_test_cases_in_file = removed_test_cases_in_file_data[
                            "removed_test_functions"
                        ]
                        filepath = removed_test_cases_in_file_data["filepath"]
                        filename = removed_test_cases_in_file_data["filename"]
                        for removed_test_case in removed_test_cases_in_file:
                            data = [
                                filepath,
                                filename,
                                removed_test_case["name"],
                                removed_test_case["check_annot"],
                            ]
                            data = [*commit_master_data, *data]
                            results.append(data)

                # Handles step 11
                elif step == 11:
                    if commit.hash not in commits_to_look:
                        continue

                    commit_hash = parse_commit_as_hyperlink(
                        label=commit.hash, url=get_full_commit_url(commit.hash)
                    )
                    # NOTE: Ignore filepath for now [causes issue for moved test file]
                    # filepaths_to_look = previous_step_df[
                    #     previous_step_df["Hash"] == commit_hash
                    # ].to_dict("list")["Filepath"]

                    filenames_to_look = previous_step_df[
                        previous_step_df["Hash"] == commit_hash
                    ].to_dict("list")["Filename"]

                    for file_idx, file in enumerate(commit.modified_files):
                        filename = file.filename
                        # NOTE: Ignore filepath for now [causes issue for moved test file]
                        # filepath = (
                        #     file.new_path
                        #     if file.new_path is not None
                        #     else file.old_path
                        # )
                        # if filepath not in filepaths_to_look:
                        #     continue

                        if filename not in filenames_to_look:
                            continue

                        # Testcases belonging to a file in a commit hash
                        data = analyzer_global.cloned_step1_hydrated_df[
                            (
                                analyzer_global.cloned_step1_hydrated_df["Hash"]
                                == commit_hash
                            )
                            & (
                                analyzer_global.cloned_step1_hydrated_df["Filename"]
                                == filename
                            )
                        ]

                        # Store all true testcases deletion in a commit [suggested by Javalang]
                        all_true_test_cases_deletion_in_commit_file = (
                            analyze_true_test_cases_deletion_in_commit_file_javaparser(
                                file
                            )
                        )

                        """
                        Filter out false positives using true positive detected by Javaparser or RegEx
                        """

                        # Javaparser does not detect true testcases deletion [i.e file cannot be parsed]
                        if all_true_test_cases_deletion_in_commit_file is None:
                            print("Voila, potential javalang parser failure detected")
                            all_testcases_deletion_in_commit_file_regex = (
                                get_removed_test_functions_regex_only(file)
                            )
                            print(
                                len(all_testcases_deletion_in_commit_file_regex),
                                "deleted testcases in file Regex",
                            )
                            
                            # Filter out using removed testcases detected by RegEx
                            if len(all_testcases_deletion_in_commit_file_regex):
                                data = data[
                                    ~data["Removed Test Case"].isin(
                                        all_testcases_deletion_in_commit_file_regex
                                    )
                                ]
                        # Javaparser detects true testcases deletion [i.e file is successfully parsed]
                        elif len(all_true_test_cases_deletion_in_commit_file):
                            print(
                                len(all_true_test_cases_deletion_in_commit_file),
                                "deleted testcases in file Javaparser",
                            )
                            data = data[
                                ~data["Removed Test Case"].isin(
                                    all_true_test_cases_deletion_in_commit_file
                                )
                            ]

                        # NOTE: If no true testcases are detected by javaparser or regex, we assume all of them are false
                        data = pd.concat(
                            [analyzer_global.cloned_step1_hydrated_df, data]
                        ).drop_duplicates(keep=False)
                        analyzer_global.cloned_step1_hydrated_df = data
                    print(
                        "Current Dataframe: ",
                        analyzer_global.cloned_step1_hydrated_df.shape,
                    )

                # Handles step 3
                elif step == 3:
                    if commit.hash not in commits_to_look:
                        continue

                    commit_hash = parse_commit_as_hyperlink(
                        label=commit.hash, url=get_full_commit_url(commit.hash)
                    )

                    all_added_test_cases_in_commit = []
                    for file_idx, file in enumerate(commit.modified_files):
                        filename = file.filename
                        # NOTE: Ignore filepath for now [causes issue for moved test file]
                        # filepath = file.new_path

                        # Store all added testcases in a commit
                        analyze_test_cases_addition_in_commit_file(
                            file, all_added_test_cases_in_commit
                        )

                    # Previously used to elimate all removed testcases with name matching with one added testcase
                    # all_added_test_cases_in_commit = list(
                    #     set(all_added_test_cases_in_commit)
                    # )

                    for added_testcase_name in all_added_test_cases_in_commit:
                        data = analyzer_global.cloned_step2_hydrated_df[
                            (
                                analyzer_global.cloned_step2_hydrated_df["Hash"]
                                == commit_hash
                            )
                            & (
                                analyzer_global.cloned_step2_hydrated_df[
                                    "Removed Test Case"
                                ]
                                == added_testcase_name
                            )
                        ]
                        
                        if not data.empty:
                            # Remove only the first matching record
                            data = data.iloc[[0]]
                            

                        data = pd.concat(
                            [analyzer_global.cloned_step2_hydrated_df, data]
                        ).drop_duplicates(keep=False)
                        analyzer_global.cloned_step2_hydrated_df = data
                    print(
                        "Current Dataframe: ",
                        analyzer_global.cloned_step2_hydrated_df.shape,
                    )

                print(
                    get_repo_name(repo_url)
                    + "......... Analyzing commit .........."
                    + commit.hash
                    + "....."
                    + commit_datetime
                )
            else:
                if step == 11:
                    # Set dataframe computed for step 11
                    analyzer_global.step11_hydrated_df = (
                        analyzer_global.cloned_step1_hydrated_df
                    )
                elif step == 3:
                    # Set dataframe computed for step 3
                    analyzer_global.step3_hydrated_df = (
                        analyzer_global.cloned_step2_hydrated_df
                    )

                is_completed = True

    def main():
        try:
            traverse_commits(analyzer_global)
            if step == 1:
                pretify_csv_results(analyzer_global)

        except ValueError as e:
            print("Analyzer: Value Error Detected")
            if analyzer_global.current_commit:
                print("Corrupted Commit ", {type(e).__name__})
                # print(analyzer_global)
                # analyzer_global.current_commit = next(analyzer_global.commits)
                analyzer_global.since = analyzer_global.since + timedelta(days=1)
                main()
            else:
                raise e
        except Exception as e:
            print("Analyzer: Exception Detected")
            raise e

    analyzer_global = AnalyzerGlobal()
    main()
    if step == 3:
        return analyzer_global.step3_hydrated_df
    elif step == 11:
        return analyzer_global.step11_hydrated_df
    else:
        return analyzer_global.results
