"""
Reads all tags in the repository and generates tags file
"""

import os.path
import os
import json

projects_list = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

for project in projects_list:
    print(project)
    print('------------')
    # First dump tags info into tags.txt file
    cmd = "git ls-remote --tags origin"
    current_state = os.getcwd()
    os.chdir(f"../io/projects/{project}")
    os.system(cmd + " > tags.txt")
    commit_tag_info_Lines = open("tags.txt", "r").readlines()

    # Parse dumped tags into a json file
    results = []
    for line in commit_tag_info_Lines:
        line = line.replace("\n", "")
        commit = line[:40]
        print(commit)
        tag = line[40:].replace(" ", "")
        print(tag)
        # Get commit datetime
        cmd = f"git log -1 --format=%ai {tag}"
        os.system(cmd + " > tmp")
        datetime = open("tmp", "r").read().replace("\n", "")
        results.append({"Hash": commit, "Tag": tag, "Datetime": datetime})
        os.remove("tmp")
    file1 = open("tags.json", "w")
    # Serializing json
    results_json = json.dumps(results, indent=4)
    file1.write(results_json)
    os.chdir(current_state)
    print("==============================================")
