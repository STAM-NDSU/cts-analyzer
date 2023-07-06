# cts-analyzer

Analyzes the git commits in the [Compatibility Test Suite (CTS)](https://source.android.com/docs/compatibility/cts) that remove the test cases.
A `<OUTPUT_Filename>_<COMMIT_START_DATE>_<COMMIT_END_DATE>.csv` file with rows containing `datetime`, `hash`, `commit msg`, `filename`, `test case`
is generated.

## Getting Started

To run the project, python should be installed on your machine.
Check if it is installed or not using

```
python --version
```

If it is not installed, download and install python from https://www.python.org/downloads/

Then, clone the repository:

```
git clone https://github.com/STAM-NDSU/cts-analyzer
cd cts-analyzer
```

Then, setup virtual environment (optional)

```
python3 -m venv venv
source venv/bin/activate
```

Then, install the requirements:

```
pip install -r requirements.txt
```

Then, create a .env file and copy the contents of .env.example

`REPO_PATH` : Url of the [cts repository](https://android.googlesource.com/platform/cts) to be analyzed or could be a local path to the repository installed on the machine
`TARGET_BRANCH` : Branch of the repository to be analyzed  
`COMMIT_START_DATE` : Start date of the target commit history  
`COMMIT_END_DATE` : End date of the target commit history. If it is not defined, it will be set to current date by default  
`CTS_COMMIT_INTERVAL` : Interval in days to auto compute `COMMIT_START_DATE`. If `COMMIT_START_DATE` is defined, it will override the interval. By default, interval is 365 days  
`OUTPUT_DIR` : Directory in the project root that will contain the generated csv file  
`OUTPUT_Filename`: Filename of the generated csv file. Default is `cts`

:warning: : `TARGET_BRANCH` should be a valid repository branch. The default branch of repository `master`. Configure accordingly in the `.env` file. Branches other than `master` should be written as `origin/<branch-name>`. Incorrect configuration will throw `GitCommandError` in the console

Finally, run following command

```
python3 main.py
```

## Terminology

- DOI(domain of interest) are the test cases removed from commits.
- Candidate files are valid test files ending with `*Test.java`

## Performance

To speed up the analysis speed, you can clone the cts repository in the project root using

```
git clone https://android.googlesource.com/platform/cts
```

And, change the CTS repository path in the .env file as

```
REPO_PATH=cts
```

## Limitations

Currently, it fails to analyze the commits for the below dates

```
07/29/2021 #mm/dd/YYYY
09/28/2021 #mm/dd/YYYY

3d7923cb734062240cddfd54594198f570243dac
ebdf728de125fb6b71008cb8e957b1ddf579b870
e65d6bebdba9df211b258fae996fe34b6eadb787

ssss
```

## Install forked pydriller
pip install -e git+https://github.com/bhattasuraj76/pydriller.git#egg=pydriller


# Git cmd to get repository stats [total commits, first and recent commit info]
To get a commit count for a revision (HEAD, master, a commit hash):

git rev-list --count <revision>

git rev-list --count master --until="2023-01-01"
git log --pretty=format:"%H - %ad - %an: %s" --until="2023-01-01" 
git log --reverse --pretty=format:"%H - %ad - %an: %s" --until="2023-01-01" 

To get the commit count across all branches:

git rev-list --all --count