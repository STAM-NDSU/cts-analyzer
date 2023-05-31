from copy import deepcopy
from datetime import timedelta
from pydriller import Repository
from . import config
from .core import analyze_test_cases_removal_in_commit_file
from .utils import (
    is_candidate_file,
    format_commit_datetime,
    get_full_commit_url,
    parse_commit_as_hyperlink,
    get_repo_name,
)

"""
  Analyze the target branch of the repository and get commits 
  that either remove tests cases and/or assertions
  from java test files that match the function definition regex 
"""

MIN_ROWS = 5
MIN_COLUMNS = 6


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
        self.total_commits = 0
        self.total_test_removal_commits = 0
        self.total_high_conf_test_removal = 0
        self.total_low_conf_test_removal = 0

    @property
    def total_testcases(self):
        return len(self.results)

    def __repr__(self) -> str:
        return f"<since={self.since} to={self.to} commit={self.current_commit.hash}"

    @classmethod
    def get_ignored_files(self, repo_url):
        ignore_files_all_projects = {
            "gson": [
                {
                    "hash": "441406cc780fc5384832b48e382a7c899bac21af",
                    "filename": "Java17RecordTest.java",
                },
                {
                    "hash": "5253ddbde0a366bb7667d94b56b0c940e465437d",
                    "filename": "Java17RecordTest.java",
                },
                {
                    "hash": "86c35bba3091afe70f38598b04ba89b7e8f539f7",
                    "filename": "Java17RecordTest.java",
                },
                {
                    "hash": "66d9621ce87c04a5167ee04097694093b13b514c",
                    "filename": "Java17RecordTest.java",
                },
            ],
            "pmd": [
                {
                    "hash": "3ee32effdaccdf2f0cf16dd200091b8b6da6c4d5",
                    "filename": "JavaEscapeReaderTest.java",
                },
                {
                    "hash": "e76a1d6eb8d32f620a567f76e4a8713a2d57a503",
                    "filename": "JavaEscapeReaderTest.java",
                },
                {
                    "hash": "0be034b3db8de0ae1cab8b0c290ab2259b520919",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "184f42e153d59df3a05bdf1f3fb011de7ec6ec7a",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "47dc6d1c961fcb5adf50b1334b08e1cf015c8011",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "a85e5c867de2a84be275bd6a7752d7d81acb8c89",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "bf6e64a1e1bebd655be75b2c9bd3ede79d262115",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "407543fd418b2978a4a48259dae662d3620ec5ac",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "4ec253a43907246435f21a6afc786001ea6f5ab1",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "0ce831fc5cab49e0a206f093b29a814c3cf383f9",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "1cf4ad8083fdfae9079cb5540dbee89fb39ac5e",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "71cf4ad8083fdfae9079cb5540dbee89fb39ac5e",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "88c3572f7cde57bb296733b847e56629c989e3f0",
                    "filename": "TypeAnnotReflectionTest.java",
                },
                {
                    "hash": "88c3572f7cde57bb296733b847e56629c989e3f0",
                    "filename": "TypeAnnotTestUtil.java",
                },
                {
                    "hash": "4621d27dfede6b7c5741cba211042a40375a198f",
                    "filename": "TypeAnnotTestUtil.java",
                },
                {
                    "hash": "dd657bad4abebc5b529f5408a9010d83fde81acf",
                    "filename": "TypeAnnotTestUtil.java",
                },
                {
                    "hash": "71b4e4459ee584bc653424786a0c2d9c255927f2",
                    "filename": "TypeAnnotTestUtil.java",
                },
                {
                    "hash": "67240f986373c6b8034a4e5b1cf104ea7464962a",
                    "filename": "TypeAnnotTestUtil.java",
                },
                {
                    "hash": "7c8aa8e5e37d7ec502397694b9d44d8c9d522432",
                    "filename": "TypeAnnotTestUtil.java",
                },
            ],
            "joda-time": [
                {
                    "hash": "a8db2e4be27585dad5c3195937a88395f4cb0314",
                    "filename": "TestParseISO.java",
                },
                {
                    "hash": "cdcbcfe055d32ad7b44f04d0ae59ceb8cbad2e28",
                    "filename": "TestParseISO.java",
                },
            ],
            "commons-lang": [
                {
                    "hash": "ce06610103cc04fa8b2dd7b61d0ef685b8900eb1",
                    "filename": "EnumTest.java",
                },
                {
                    "hash": "ce06610103cc04fa8b2dd7b61d0ef685b8900eb1",
                    "filename": "EnumTestSuite.java",
                },
                {
                    "hash": "ce06610103cc04fa8b2dd7b61d0ef685b8900eb1",
                    "filename": "EnumUtilsTest.java",
                },
                {
                    "hash": "ce06610103cc04fa8b2dd7b61d0ef685b8900eb1",
                    "filename": "ValuedEnumTest.java",
                },
                {
                    "hash": "ad50195441954aaf63f87bad97447b219bbbc7d",
                    "filename": "EnumTest.java",
                },
                {
                    "hash": "1ad50195441954aaf63f87bad97447b219bbbc7d",
                    "filename": "EnumTest.java",
                },
                {
                    "hash": "1ad50195441954aaf63f87bad97447b219bbbc7d",
                    "filename": "ValuedEnumTest.java",
                },
                {
                    "hash": "b0d8436ce85d7d681e5f90215e6a6aac9657a013",
                    "filename": "EnumTest.java",
                },
                {
                    "hash": "27c8d12495566b4401bcb20129889094baf97428",
                    "filename": "EnumTest.java",
                },
                {
                    "hash": "2f50297e5eb582ed50e87e6801917abe5a30b3c1",
                    "filename": "EnumTest.java",
                },
                {
                    "hash": "85cbed66ff3353d034568764cc91c30e1aafad26",
                    "filename": "EnumTest.java",
                },
                {
                    "hash": "ccde85985d2cd95afc21ff2a0f9e274b613c77a2",
                    "filename": "EnumUtilsTest.java",
                },
                {
                    "hash": "e7d21364b5dc746f7086aef1ad6a0e1851ced2f4",
                    "filename": "EnumTest.java",
                },
                {
                    "hash": "04e9eb14e7f5dbf55ba41819b9cb2d2f0c3c4b55",
                    "filename": "AllLangTestSuite.java",
                },
            ],
            "commons-math": [
                {
                    "hash": "05195b77ca8d86fbb4fdd9216f436d8b7f3a57de",
                    "filename": "MappableArrayTest.java",
                },
                {
                    "hash": "05195b77ca8d86fbb4fdd9216f436d8b7f3a57de",
                    "filename": "MappableScalarTest.java",
                },
                {
                    "hash": "cc73bfb42fa86c01e37a1b7021b1ab41e0f0cb63",
                    "filename": "MappableArrayTest.java",
                },
                {
                    "hash": "b24f72809bfdc17ac7e9dd4114208f36b319ea80",
                    "filename": "MappableScalarTest.java",
                },
            ],
            "cts": [
                {
                    "hash": "ba5ee4af0bbf73368270c27567cbd1787f1a321c",
                    "filename": "PackageManagerShellCommandTest.java",
                },
                {
                    "hash": "ba5ee4af0bbf73368270c27567cbd1787f1a321c",
                    "filename": "ConfigurationTest.java",
                },
                {
                    "hash": "035b45369db9863114b369f50911204a13b7c4be",
                    "filename": "ConfigurationTest.java",
                },
                {
                    "hash": "0f2f187b768f0ee09ed52fd476d0c0df80ab9bef",
                    "filename": "PackageManagerShellCommandTest.java",
                },
                {
                    "hash": "4a06faf9b60f61e37e2d661beac75b845e3e5bf1",
                    "filename": "PackageManagerShellCommandTest.java",
                },
                {
                    "hash": "5ee7e2c15f67074e3684b7408ebecae986413fd0",
                    "filename": "PackageManagerShellCommandTest.java",
                },
                {
                    "hash": "aecdd4554625022277deee46dfe377840f013329",
                    "filename": "PackageManagerShellCommandTest.java",
                },
                {
                    "hash": "20b890d8099e2f91e9b27dc2d53f2ee5ea00ae02",
                    "filename": "PackageManagerShellCommandTest.java",
                },
            ],
        }
        if get_repo_name(repo_url) in ignore_files_all_projects:
            return ignore_files_all_projects[get_repo_name(repo_url)]
        else:
            return []


def get_removed_test_functions_and_assertions_details(repo_url, branch, repo_refactors):
    def pretify_csv_results(analyzer_global):
        results = analyzer_global.results
        if len(results) < MIN_ROWS:
            fill_rows = MIN_ROWS - len(results)
            fill_columns = MIN_COLUMNS
            filled_rows = [[" "] * fill_columns for _ in range(0, fill_rows)]
            results = results + filled_rows
        results[0].insert(6, "Total Commits")
        results[0].insert(7, analyzer_global.total_commits)
        results[1].insert(6, "Total Commits Test Removal")
        results[1].insert(7, analyzer_global.total_test_removal_commits)
        results[2].insert(6, "Total High")
        results[2].insert(7, analyzer_global.total_high_conf_test_removal)
        results[3].insert(6, "Total Low")
        results[3].insert(7, analyzer_global.total_low_conf_test_removal)
        results[4].insert(6, "Total Testcases")
        results[4].insert(7, analyzer_global.total_testcases)

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
            # single="213e37f2a4b1ac04c138b01de54b933a45086967",  # use it only for debugging
        ).traverse_commits()
        analyzer_global.commits = commits

        if not commits:
            print("No Commits---- Oopss")

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
                analyzer_global.total_commits += 1
                # Update current_commit pointer; to skip the corrupted ones
                analyzer_global.current_commit = commit
                analyzer_global.since = commit.committer_date

                commit_datetime = format_commit_datetime(commit.committer_date)
                commit_hash = parse_commit_as_hyperlink(
                    label=commit.hash, url=get_full_commit_url(commit.hash)
                )

                commit_msg = commit.msg
                commit_master_data = [commit_datetime, commit_hash, commit_msg]
                empty_commit_master_data = ["", "", ""]

                commit_included = False
                # Holds all test cases across multiple modified files; helps to eliminate
                # considering moved test cases having same name
                all_added_test_cases_in_commit = []
                all_removed_test_cases_in_commit = []

                for file_idx, file in enumerate(commit.modified_files):
                    filename = file.filename
                    # Check if file is a candidate file
                    if not is_candidate_file(filename):
                        continue

                    print(
                        "..................... Analyzing file .........."
                        + file.filename
                    )

                    # Skip for files with compilation error(could not be parsed by JavaParser) [quick fix]
                    ignored_files = analyzer_global.get_ignored_files(repo_url)

                    should_skip = any(
                        each["hash"] == commit.hash and each["filename"] == filename
                        for each in ignored_files
                    )
                    # def filter_ignore_file(file_data):
                    #     print(
                    #         file_data["hash"],
                    #         commit.hash,
                    #         file_data["hash"] == commit.hash,
                    #         file_data["filename"] == filename,
                    #     )
                    #     return (
                    #         file_data["hash"] == commit.hash
                    #         and file_data["filename"] == filename
                    #     )

                    # should_skip = list(
                    #     filter(
                    #         filter_ignore_file,
                    #         ignored_files,
                    #     )
                    # )

                    if should_skip:
                        continue

                    # This is where MAGIC happens
                    all_removed_test_cases_file_data = (
                        analyze_test_cases_removal_in_commit_file(
                            file, all_added_test_cases_in_commit
                        )
                    )
                    all_removed_test_cases_file_data["file_index"] = file_idx
                    all_removed_test_cases_file_data["filename"] = filename
                    all_removed_test_cases_file_data["filepath"] = file.old_path
                    all_removed_test_cases_in_commit.append(
                        all_removed_test_cases_file_data
                    )

                # Prune moved and refactored test files
                temp_all_removed_test_cases_in_commit = deepcopy(
                    all_removed_test_cases_in_commit
                )
                for index, removed_test_cases_in_file_data in enumerate(
                    all_removed_test_cases_in_commit
                ):
                    removed_test_cases_in_file = removed_test_cases_in_file_data[
                        "removed_test_functions"
                    ]
                    if not removed_test_cases_in_file:
                        continue

                    for removed_test_case in removed_test_cases_in_file:
                        # Filter out moved test cases(across files in commit) from removed test cases [Hypothesis 3]
                        if config.HANDLE_MOVED == "true":
                            if removed_test_case in all_added_test_cases_in_commit:
                                temp_all_removed_test_cases_in_commit[index][
                                    "removed_test_functions"
                                ].remove(removed_test_case)

                        # Filter our refactored test cases [ suggested by RefMiner]
                        if config.HANDLE_REFACTOR == "true":
                            # refactors_commit_data = list(filter(lambda each: each["sha1"] == commit.hash, repo_refactors))[0]
                            refactors_commit_data = next(
                                (
                                    each
                                    for each in repo_refactors
                                    if each["sha1"] == commit.hash
                                ),
                                None,
                            )
                            refactors_commit = (
                                refactors_commit_data["refactorings"]
                                if not refactors_commit_data is None
                                else []
                            )
                            # print("no", refactor["refactors_commit"])
                            for refactor in refactors_commit:
                                for each in refactor["leftSideLocations"]:
                                    # Check if removed test function is in refactored codeElement of same file path
                                    # print(each["filePath"])
                                    # print(temp_all_removed_test_cases_in_commit[index]["filepath"])
                                    if (
                                        each["codeElement"]
                                        and removed_test_case in each["codeElement"]
                                        and removed_test_case
                                        in temp_all_removed_test_cases_in_commit[index][
                                            "removed_test_functions"
                                        ]
                                        and temp_all_removed_test_cases_in_commit[
                                            index
                                        ]["filepath"]
                                        == each["filePath"]
                                    ):
                                        temp_all_removed_test_cases_in_commit[index][
                                            "removed_test_functions"
                                        ].remove(removed_test_case)

                    all_removed_test_cases_in_commit = (
                        temp_all_removed_test_cases_in_commit
                    )
                for (
                    rm_test_case_file_data_idx,
                    removed_test_cases_in_file_data,
                ) in enumerate(all_removed_test_cases_in_commit):
                    removed_test_cases_in_file = removed_test_cases_in_file_data[
                        "removed_test_functions"
                    ]
                    confidence = removed_test_cases_in_file_data["confidence"]
                    filename = removed_test_cases_in_file_data["filename"]
                    for removed_test_case_idx_in_file, removed_test_case in enumerate(
                        removed_test_cases_in_file
                    ):
                        if rm_test_case_file_data_idx == 0:
                            if removed_test_case_idx_in_file == 0:
                                data = [filename, removed_test_case, confidence]
                                data = [*commit_master_data, *data]

                                # Compute key stats
                                analyzer_global.total_test_removal_commits += 1
                                if confidence == "HIGH":
                                    analyzer_global.total_high_conf_test_removal += 1
                                else:
                                    analyzer_global.total_low_conf_test_removal += 1

                                # Toggle commit included flag
                                commit_included = True
                            else:
                                data = ["", removed_test_case, ""]
                                data = [*empty_commit_master_data, *data]
                        else:
                            if removed_test_case_idx_in_file == 0:
                                data = [filename, removed_test_case, confidence]
                                if commit_included:
                                    data = [*empty_commit_master_data, *data]
                                else:
                                    data = [*commit_master_data, *data]
                                    # Toggle commit included flag
                                    commit_included = True
                                # Compute key stats
                                analyzer_global.total_test_removal_commits += 1
                                if confidence == "HIGH":
                                    analyzer_global.total_high_conf_test_removal += 1
                                else:
                                    analyzer_global.total_low_conf_test_removal += 1
                            else:
                                data = ["", removed_test_case, ""]
                                data = [*empty_commit_master_data, *data]
                        results.append(data)

            else:
                is_completed = True

    analyzer_global = AnalyzerGlobal()

    def main():
        try:
            traverse_commits(analyzer_global)
            pretify_csv_results(analyzer_global)
            return analyzer_global.results
        except ValueError as e:
            print("Analyzer: Value Error Detected")
            if analyzer_global.current_commit:
                print("Corrupted Commit ", {type(e).__name__})
                print(analyzer_global)
                # analyzer_global.current_commit = next(analyzer_global.commits)
                analyzer_global.since = analyzer_global.since + timedelta(days=1)
                main()
                return analyzer_global.results
        except Exception as e:
            print("Analyzer: Exception Detected")
            raise e

    main()

    return analyzer_global.results
