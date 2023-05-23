from copy import deepcopy
from datetime import timedelta
from pydriller import Repository
from . import config
from .core import analyze_test_cases_removal_in_commit_file
from .utils import is_candidate_file, format_commit_datetime, get_full_commit_url, \
    parse_commit_as_hyperlink, get_repo_name

"""
  Analyze the target branch of the repository and get commits 
  that either remove tests cases and/or assertions
  from java test files that match the function definition regex 
"""

MIN_ROWS = 3
MIN_COLUMNS = 6


class AnalyzerGlobal:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AnalyzerGlobal, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.since= config.COMMIT_START_DATETIME
        self.to=config.COMMIT_END_DATETIME
        self.commits = None
        self.current_commit=None
        self.results = []
        self.total_commit_test_removal = 0
        self.total_high_conf_test_removal = 0
        self.total_low_conf_test_removal = 0
        
    def __repr__(self) -> str:
        return f"<since={self.since} to={self.to} commit={self.current_commit.hash}"
       
            
def get_removed_test_functions_and_assertions_details(repo_url, branch, repo_refactors):

    
    def pretify_csv_results(analyzer_global):
        results = analyzer_global.results
        if len(results) < MIN_ROWS:
            fill_rows = MIN_ROWS - len(results)
            fill_columns = MIN_COLUMNS
            filled_rows = [[" "] * fill_columns for _ in range(0, fill_rows)]
            results = results + filled_rows

        results[0].insert(6, "Total Commits")
        results[0].insert(7, analyzer_global.total_commit_test_removal)
        results[1].insert(6, "Total High")
        results[1].insert(7, analyzer_global.total_high_conf_test_removal)
        results[2].insert(6, "Total Low")
        results[2].insert(7, analyzer_global.total_low_conf_test_removal)
        
    def traverse_commits(analyzer_global):
        since= analyzer_global.since
        to= analyzer_global.to
        results = analyzer_global.results
        total_commit_test_removal = analyzer_global.total_commit_test_removal
        commits = Repository(repo_url, only_in_branch=branch,
                            only_modifications_with_file_types=config.JAVA_FILE_EXT,
                            # since=since, to=to,
                            single="fb761ffb51ba1436163b094255b6af40bf69bd83",  # use it only for debugging
                            ).traverse_commits()
        analyzer_global.commits = commits
        
        if not commits:
            print("No Commits--- Oops")
            
        is_completed = False
        while(not is_completed):
            commit = next(commits, None)
            if commit:            
                # Update current_commit pointer; to skip the corrupted ones
                analyzer_global.current_commit = commit
                analyzer_global.since = commit.committer_date
                
                commit_datetime = format_commit_datetime(commit.committer_date)
                commit_hash = parse_commit_as_hyperlink(label=commit.hash,
                                                        url=get_full_commit_url(commit.hash))

                commit_msg = commit.msg
                commit_master_data = [commit_datetime, commit_hash, commit_msg]
                empty_commit_master_data = ['', '', '']

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

                    all_removed_test_cases_file_data = analyze_test_cases_removal_in_commit_file(
                        file, all_added_test_cases_in_commit)
                    all_removed_test_cases_file_data["file_index"] = file_idx
                    all_removed_test_cases_file_data["filename"] = filename
                    all_removed_test_cases_in_commit.append(all_removed_test_cases_file_data)

                # Prune moved and refactored test files
                temp_all_removed_test_cases_in_commit = deepcopy(all_removed_test_cases_in_commit)
                for index, removed_test_cases_in_file_data in enumerate(all_removed_test_cases_in_commit):
                    removed_test_cases_in_file = removed_test_cases_in_file_data["removed_test_functions"]
                    if not removed_test_cases_in_file:
                        continue
                    
                    for removed_test_case in removed_test_cases_in_file:
                        # Filter out moved test cases(across files in commit) from removed test cases
                        if config.HANDLE_MOVED == "true":
                            if removed_test_case in all_added_test_cases_in_commit:
                                temp_all_removed_test_cases_in_commit[index]["removed_test_functions"].remove(removed_test_case)

                        # Filter our refactored test cases
                        if config.HANDLE_REFACTOR == "true":
                            # refactors_commit_data = list(filter(lambda each: each["sha1"] == commit.hash, repo_refactors))[0]
                            refactors_commit_data = next((each for each in repo_refactors if each["sha1"] == commit.hash), None)
                            refactors_commit = refactors_commit_data["refactorings"] if not refactors_commit_data is None else []
                            # print("no", refactor["refactors_commit"])
                            for refactor in refactors_commit:
                                for each in refactor["leftSideLocations"]:
                                    if each["codeElement"] and removed_test_case in each["codeElement"] \
                                            and removed_test_case in \
                                            temp_all_removed_test_cases_in_commit[index]["removed_test_functions"]:
                                        temp_all_removed_test_cases_in_commit[index]["removed_test_functions"].remove(
                                            removed_test_case)

                    all_removed_test_cases_in_commit = temp_all_removed_test_cases_in_commit
                for rm_test_case_file_data_idx, removed_test_cases_in_file_data in enumerate(
                        all_removed_test_cases_in_commit):
                    removed_test_cases_in_file = removed_test_cases_in_file_data["removed_test_functions"]
                    confidence = removed_test_cases_in_file_data["confidence"]
                    filename = removed_test_cases_in_file_data["filename"]
                    for removed_test_case_idx_in_file, removed_test_case in enumerate(removed_test_cases_in_file):
                        if rm_test_case_file_data_idx == 0:
                            if removed_test_case_idx_in_file == 0:
                                data = [
                                    filename,
                                    removed_test_case,
                                    confidence
                                ]
                                data = [*commit_master_data, *data]

                                # Compute key stats
                                analyzer_global.total_commit_test_removal += 1
                                if confidence == "HIGH":
                                    analyzer_global.total_high_conf_test_removal += 1
                                else:
                                    analyzer_global.total_low_conf_test_removal += 1

                                # Toggle commit included flag
                                commit_included = True
                            else:
                                data = [
                                    '',
                                    removed_test_case,
                                    ''
                                ]
                                data = [*empty_commit_master_data, *data]
                        else:
                            if removed_test_case_idx_in_file == 0:
                                data = [
                                    filename,
                                    removed_test_case,
                                    confidence
                                ]
                                if commit_included:
                                    data = [*empty_commit_master_data, *data]
                                else:
                                    data = [*commit_master_data, *data]
                                    # Toggle commit included flag
                                    commit_included = True
                                # Compute key stats
                                analyzer_global.total_commit_test_removal += 1
                                if confidence == "HIGH":
                                    analyzer_global.total_high_conf_test_removal += 1
                                else:
                                    analyzer_global.total_low_conf_test_removal += 1
                            else:
                                data = [
                                    '',
                                    removed_test_case,
                                    ''
                                ]
                                data = [*empty_commit_master_data, *data]
                        results.append(
                            data
                        )
                print(get_repo_name(repo_url) + \
                        "......... Analyzing commit .........." + commit.hash + '.....' + commit_datetime)
            else:
                is_completed = True

    
    analyzer_global =  AnalyzerGlobal()
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
    

# 29d9255f668b8da42fc4fcd40b2a5e716b9b7a53