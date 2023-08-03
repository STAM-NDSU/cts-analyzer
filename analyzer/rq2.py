from copy import deepcopy
from datetime import timedelta
from pydriller import Repository
import pandas as pd
from . import config
from .racore import (
    analyze_functions_removal_in_commit_file,
    analyze_functions_referenced_in_removed_testcase,
)
from .utils import (
    is_candidate_test_file,
    format_commit_datetime,
    parse_commit_as_hyperlink_by_project,
    get_repo_name,
    strip_commit_url,
)
from operator import itemgetter


"""
  Analyze the target branch of the repository to identify functions referenced by removed testcase and
  other details 
"""


class AnalyzerGlobal:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(AnalyzerGlobal, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.since = config.COMMIT_START_DATETIME
        self.to = config.COMMIT_END_DATETIME
        self.commits = None
        self.current_commit = None
        self.results = []
        self.test_deletion_hydrated_df = None

    @property
    def total_results(self):
        return len(self.results)

    def __repr__(self) -> str:
        return f"<since={self.since} to={self.to} commit={self.current_commit.hash}"


def get_removed_testcase_and_referenced_functions_details(
    project, repo_url, branch, test_deletion_hydrated_df=None
):
    def traverse_commits(analyzer_global):
        since = analyzer_global.since
        to = analyzer_global.to
        commits = Repository(
            repo_url,
            only_in_branch=branch,
            only_modifications_with_file_types=config.JAVA_FILE_EXT,
            since=since,
            to=to,
            only_no_merge=True,
            # single="b9998e511f3a3c19d52c104d66d78037eaff88ec",  # use it only for debugging
        ).traverse_commits()
        analyzer_global.commits = commits

        if not commits:
            print("No Commits---- Oopss")

        test_deletion_hydrated_df["Referenced Functions"] = None
        test_deletion_hydrated_df["Deleted With Source Code"] = None
        test_deletion_hydrated_df["Deleted With Whole File"] = None
        analyzer_global.test_deletion_hydrated_df = test_deletion_hydrated_df
        print("Initial Dataframe: ", test_deletion_hydrated_df.shape)

        if test_deletion_hydrated_df is not None:
            # Check for all the validation commits
            commits_to_look = test_deletion_hydrated_df.to_dict("list")["Hash"]
            commits_hash_to_look = list(
                set(list(map(lambda each: strip_commit_url(each), commits_to_look)))
            )
            print("Total commits to scan: ", len(commits_to_look))

        is_completed = False
        all_data = []
        while not is_completed:
            commit = next(commits, None)
            if commit:
                commit_datetime = format_commit_datetime(commit.committer_date)
                commit_hash = parse_commit_as_hyperlink_by_project(project, commit.hash)
                # Update current_commit pointer; to skip the corrupted ones
                analyzer_global.current_commit = commit
                analyzer_global.since = commit.committer_date

                # Check if commit hash is valid test deletion commit hash
                if commit.hash not in commits_hash_to_look:
                    continue

                # Compute all removed functions across modified files;
                all_removed_functions_in_commit = []
                for file_idx, file in enumerate(commit.modified_files):
                    filename = file.filename
                    # Check if file is a candidate test file (statifies test file pattern); ignore it
                    if is_candidate_test_file(filename):
                        continue

                    all_removed_functions_in_file = (
                        analyze_functions_removal_in_commit_file(file)
                    )

                    all_removed_functions_in_commit = [
                        *all_removed_functions_in_commit,
                        *all_removed_functions_in_file,
                    ]
                print("removed methods", len(all_removed_functions_in_commit))

                test_deletion_filenames = test_deletion_hydrated_df[
                    test_deletion_hydrated_df["Hash"] == commit_hash
                ].to_dict("list")["Filename"]
                test_deletion_filenames = list(set(test_deletion_filenames))
                print("filenames to look", test_deletion_filenames)

                for file_idx, file in enumerate(commit.modified_files):
                    filename = file.filename

                    # Check if file matches test deletion containing file; ignore if does not matches
                    if filename not in test_deletion_filenames:
                        continue

                    # Deleted testcases belonging to a file in a commit hash
                    deleted_testcase_in_file_df = (
                        analyzer_global.test_deletion_hydrated_df[
                            (
                                analyzer_global.test_deletion_hydrated_df["Hash"]
                                == commit_hash
                            )
                            & (
                                analyzer_global.test_deletion_hydrated_df["Filename"]
                                == filename
                            )
                        ]
                    )
                    print("deleted testcase", len(deleted_testcase_in_file_df), filename)

                    all_data = []
                    for index, row in deleted_testcase_in_file_df.iterrows():
                        # Check if whole file is deleted
                        if file.new_path is None:
                            row["Deleted With Whole File"] = "yes"
                        else:
                            row["Deleted With Whole File"] = "no"
                            
                        removed_test_case = row["Removed Test Case"]
                        print("removed testcase", filename, removed_test_case)
                        functions_referenced = (
                            analyze_functions_referenced_in_removed_testcase(
                                file, removed_test_case
                            )
                        )
                        # Check if testcase is deleted along with source code[Test if javaparser successfully parses]
                        if functions_referenced is None:
                            row["Deleted With Source Code"] = "undecided"
                            print("Javaparser failed for :", commit.hash, filename)
                        else:
                            print("Functions reference", functions_referenced)
                            row["Referenced Functions"] = ",".join(functions_referenced)
                            # Check if 
                            match_found = False
                            for function_referenced in functions_referenced:
                                if function_referenced in all_removed_functions_in_commit:
                                    match_found = True
                                    break

                            if match_found:
                                row["Deleted With Source Code"] = "yes"
                            else:
                                row["Deleted With Source Code"] = "no"
                        

                        data = [
                            row["Datetime"],
                            row["Hash"],
                            row["Author"],
                            row["Commit Msg"],
                            row["Filepath"],
                            row["Filename"],
                            row["Removed Test Case"],
                            row["Referenced Functions"],
                            row["Deleted With Source Code"],
                            row["Deleted With Whole File"],
                        ]
                        all_data.append(data)

                print(
                    get_repo_name(repo_url)
                    + "......... Analyzing commit .........."
                    + commit.hash
                    + "....."
                    + commit_datetime
                )
            else:
                # Set dataframe computed as results
                new_df = pd.DataFrame(
                    data=all_data,
                    columns=[
                        "Datetime",
                        "Hash",
                        "Author",
                        "Commit Msg",
                        "Filepath",
                        "Filename",
                        "Removed Test Case",
                        "Referenced Functions",
                        "Deleted With Source Code",
                        "Deleted With Whole File",
                    ],
                )
                analyzer_global.results = new_df

                is_completed = True

    def main():
        try:
            traverse_commits(analyzer_global)

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
    return analyzer_global.results
