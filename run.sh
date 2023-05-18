#!/bin/bash

projects=(
         "io/projects/commons-lang__master__https://github.com/apache/commons-lang/commit/__io/outputRevisedLatest2/commons-lang__commons-lang-step1__false__commons-lang.json__false"
         "io/projects/commons-lang__master__https://github.com/apache/commons-lang/commit/__io/outputRevisedLatest2/commons-lang__commons-lang-step2__true__commons-lang.json__false"
         "io/projects/commons-lang__master__https://github.com/apache/commons-lang/commit/__io/outputRevisedLatest2/commons-lang__commons-lang-step3__true__commons-lang.json__true"

         "io/projects/joda-time__main__https://github.com/JodaOrg/joda-time/commit/__io/outputRevisedLatest2/joda-time__joda-time-step1__false__joda-time.json__false"
         "io/projects/joda-time__main__https://github.com/JodaOrg/joda-time/commit/__io/outputRevisedLatest2/joda-time__joda-time-step2__true__joda-time.json__false"
         "io/projects/joda-time__main__https://github.com/JodaOrg/joda-time/commit/__io/outputRevisedLatest2/joda-time__joda-time-step3__true__joda-time.json__true"

        #  "io/projects/pmd__master__https://github.com/pmd/pmd/commit/__io/outputRevisedLatest2/pmd__pmd-step1__false__pmd.json__false"
        #  "io/projects/pmd__master__https://github.com/pmd/pmd/commit/__io/outputRevisedLatest2/pmd__pmd-step2__true__pmd.json__false"
        #  "io/projects/pmd__master__https://github.com/pmd/pmd/commit/__io/outputRevisedLatest2/pmd__pmd-step3__true__pmd.json__true"

         "io/projects/gson__master__https://github.com/google/gson/commit/__io/outputRevisedLatest2/gson__gson-step1__false__gson.json__false"
         "io/projects/gson__master__https://github.com/google/gson/commit/__io/outputRevisedLatest2/gson__gson-step2__true__gson.json__false"
         "io/projects/gson__master__https://github.com/google/gson/commit/__io/outputRevisedLatest2/gson__gson-step3__true__gson.json__true"

         "io/projects/commons-math__master__https://github.com/apache/commons-math/commit/__io/outputRevisedLatest2/commons-math__commons-math-step1__false__commons-math.json__false"
         "io/projects/commons-math__master__https://github.com/apache/commons-math/commit/__io/outputRevisedLatest2/commons-math__commons-math-step2__true__commons-math.json__false"
         "io/projects/commons-math__master__https://github.com/apache/commons-math/commit/__io/outputRevisedLatest2/commons-math__commons-math-step3__true__commons-math.json__true"
        
         "io/projects/jfreechart__master__https://github.com/jfree/jfreechart/commit/__io/outputRevisedLatest2/jfreechart__jfreechart-step1__false__jfreechart.json__false"
         "io/projects/jfreechart__master__https://github.com/jfree/jfreechart/commit/__io/outputRevisedLatest2/jfreechart__jfreechart-step2__true__jfreechart.json__false"
         "io/projects/jfreechart__master__https://github.com/jfree/jfreechart/commit/__io/outputRevisedLatest2/jfreechart__jfreechart-step3__true__jfreechart.json__true"
        
        #  "io/projects/cts__master__https://android.googlesource.com/platform/cts/+/__io/outputRevisedLatest2/cts__cts-step1__false__cts.json__false"
        #  "io/projects/cts__master__https://android.googlesource.com/platform/cts/+/__io/outputRevisedLatest2/cts__cts-step2__true__cts.json__false"
        #  "io/projects/cts__master__https://android.googlesource.com/platform/cts/+/__io/outputRevisedLatest2/cts__cts-step3__true__cts.json__true"
        

             )

for project_data in "${projects[@]}"
do
    set -f # avoid globbing (expansion of *).
    project_arr=(${project_data//__/ }) # ${string//substring/replacement}
#    for j in "${!project_arr[@]}" # converts into array of index 0, 1
#    do
#      echo "${date_arr[j]}"
#    done
    CTS_REPO_PATH="${project_arr[0]}"  CTS_TARGET_BRANCH="${project_arr[1]}" CTS_COMMIT_BASE_URL="${project_arr[2]}" CTS_COMMIT_START_DATE="01/01/2000" CTS_COMMIT_END_DATE="01/01/2023" OUTPUT_DIR="${project_arr[3]}" OUTPUT_FILENAME="${project_arr[4]}" HANDLE_REFACTOR="${project_arr[5]}" REFACTOR_FILE="${project_arr[6]}" HANDLE_MOVED="${project_arr[7]}" HANDLE_EXPORT="true" nohup python3 main.py &
done
