from copy import deepcopy
from datetime import timedelta
from pydriller import Repository
import pandas as pd
from . import config
from .ra2core import (
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
import traceback
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
        self.results_df = []
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
        test_deletion_hydrated_df["Deleted With Source Code Decision"] = "decided" # If further manual validation is required to conform deletion with source code
        test_deletion_hydrated_df["Deleted With Whole File"] = None
        
        # analyzer_global.test_deletion_hydrated_df = test_deletion_hydrated_df
        print("Initial Dataframe: ", test_deletion_hydrated_df.shape)
        if test_deletion_hydrated_df is not None:
            # Check for all the validation commits
            commits_to_look = list(test_deletion_hydrated_df["Hash"].dropna().unique())
            commits_hash_to_look = list(
                map(lambda each: strip_commit_url(each), commits_to_look)
            )

            print("Total commits to scan: ", len(commits_to_look))

        is_completed = False

        while not is_completed:
            commit = next(commits, None)
            if commit:
                print(
                    get_repo_name(repo_url)
                    + "......... Analyzing commit .........."
                    + commit.hash
                    + "....."
                    + format_commit_datetime(commit.committer_date)
                )
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
                    
                    # Ignore if file is a candidate test file (statifies test file pattern);
                    if is_candidate_test_file(filename):
                        continue
                    print("here2")
                    all_removed_functions_in_file = (
                        analyze_functions_removal_in_commit_file(file)
                    )
                    
                    if all_removed_functions_in_file:
                        all_removed_functions_in_commit = [
                            *all_removed_functions_in_commit,
                            *all_removed_functions_in_file,
                        ]
                
                # Get all filenames containing deleted test from matching hash
                test_deletion_filepaths = test_deletion_hydrated_df[
                    test_deletion_hydrated_df["Hash"] == commit_hash
                ].to_dict("list")["Filepath"]
                test_deletion_filepaths = list(set(test_deletion_filepaths))
                
                # Compute referenced methods for deleted testcases
                for file_idx, file in enumerate(commit.modified_files):
                    filename = file.filename
                    filepath = file.old_path

                    # Ignore if test deletion filepath does not matches test deletion filepath;
                    if filepath not in test_deletion_filepaths:
                        continue

                    # Deleted testcases belonging to a file in a commit hash
                    deleted_testcase_in_file_df = test_deletion_hydrated_df[
                        (test_deletion_hydrated_df["Hash"] == commit_hash)
                        & (test_deletion_hydrated_df["Filepath"] == filepath)
                        & (test_deletion_hydrated_df["Filename"] == filename)
                    ]

                    for index, row in deleted_testcase_in_file_df.iterrows():
                        new_data = {}
                        # Check if whole file is deleted
                        if file.new_path is None:
                            new_data["Deleted With Whole File"] = "yes"
                        else:
                            new_data["Deleted With Whole File"] = "no"

                        removed_test_case = row["Removed Test Case"]
                        
                        functions_referenced = (
                            analyze_functions_referenced_in_removed_testcase(
                                file, removed_test_case
                            )
                        )
                        
                        # Check if testcase is deleted along with source code[Test if javaparser successfully parses]
                        if functions_referenced is None or len(functions_referenced) == 0:
                            new_data["Referenced Functions"] = ""
                            # TODO: CHANGE LOGIC HERE FOR QUICK FIX
                            new_data["Deleted With Source Code"] = "yes"
                            new_data["Deleted With Source Code Decision"] = "undecided"
                            print("Javaparser failed for :", commit.hash, filename)
                        else:
                            new_data["Referenced Functions"] = ",".join(
                                functions_referenced
                            )
                            # Check if
                            match_found = False
                            for function_referenced in functions_referenced:
                                if (
                                    function_referenced
                                    in all_removed_functions_in_commit
                                ):
                                    match_found = True
                                    break

                            if match_found:
                                new_data["Deleted With Source Code"] = "yes"
                            else:
                                new_data["Deleted With Source Code"] = "no"
                            new_data["Deleted With Source Code Decision"] = "decided"
                            
                        data = [
                            row["Datetime"],
                            row["Hash"],
                            row["Parent"],
                            row["Author"],
                            row["Commit Msg"],
                            row["Filepath"],
                            row["Filename"],
                            row["Removed Test Case"],
                            new_data["Referenced Functions"],
                            new_data["Deleted With Source Code"],
                            new_data["Deleted With Source Code Decision"],
                            new_data["Deleted With Whole File"],
                        ]
                        analyzer_global.results.append(data)

                print(
                    get_repo_name(repo_url)
                    + "......... Analyzed commit .........."
                    + commit.hash
                    + "....."
                    + format_commit_datetime(commit.committer_date)
                )
                print("All data length", len(analyzer_global.results))
                print("-----------xxxxxx--------------")
            else:
                # Set dataframe computed as results
                new_df = pd.DataFrame(
                    data=analyzer_global.results,
                    columns=[
                        "Datetime",
                        "Hash",
                        "Parent",
                        "Author",
                        "Commit Msg",
                        "Filepath",
                        "Filename",
                        "Removed Test Case",
                        "Referenced Functions",
                        "Deleted With Source Code",
                        "Deleted With Source Code Decision",
                        "Deleted With Whole File",
                    ],
                )
                analyzer_global.results_df = new_df

                is_completed = True

    def main():
        try:
            traverse_commits(analyzer_global)

        except ValueError as e:
            traceback.print_exc()
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
            traceback.print_exc()
            raise e

    analyzer_global = AnalyzerGlobal()
    main()
    return analyzer_global.results_df
