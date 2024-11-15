#!/bin/bash

projects=(
          # "../os-java-projects/commons-lang__master__https://github.com/apache/commons-lang/commit/__io/artifacts/commons-lang__commons-lang_step1__commons-lang.json__true"
        #   "../os-java-projects/joda-time__main__https://github.com/JodaOrg/joda-time/commit/__io/artifacts/joda-time__joda-time__step1__joda-time.json__true"
        #   "../os-java-projects/pmd__master__https://github.com/pmd/pmd/commit/__io/artifacts/pmd__pmd__step1__pmd.json__true"
        #   "../os-java-projects/gson__master__https://github.com/google/gson/commit/__io/artifacts/gson__gson__step1__gson.json__true"
          # "../os-java-projects/commons-math__master__https://github.com/apache/commons-math/commit/__io/artifacts/commons-math__commons-math__step1_commons-math.json__true"
        #   "../os-java-projects/jfreechart__master__https://github.com/jfree/jfreechart/commit/__io/artifacts/jfreechart__jfreechart__step1__jfreechart.json__true"
          # "../os-java-projects/cts__master__https://android.googlesource.com/platform/cts/+/__io/artifacts/cts__cts__step1__cts.json__true"
       
         "../os-java-projects/commons-lang__master__https://github.com/apache/commons-lang/commit/__io/artifacts/commons-lang__commons-lang__step2__commons-lang.json__true"
         "../os-java-projects/joda-time__main__https://github.com/JodaOrg/joda-time/commit/__io/artifacts/joda-time__joda-time__step2__joda-time.json__true"
         "../os-java-projects/pmd__master__https://github.com/pmd/pmd/commit/__io/artifacts/pmd__pmd__step2__pmd.json__true"
         "../os-java-projects/gson__master__https://github.com/google/gson/commit/__io/artifacts/gson__gson__step2__gson.json__true"
         "../os-java-projects/commons-math__master__https://github.com/apache/commons-math/commit/__io/artifacts/commons-math__commons-math__step2__commons-math.json__true"
         "../os-java-projects/jfreechart__master__https://github.com/jfree/jfreechart/commit/__io/artifacts/jfreechart__jfreechart__step2__jfreechart.json__true"
         "../os-java-projects/cts__master__https://android.googlesource.com/platform/cts/+/__io/artifacts/cts__cts__step2__cts.json__true"

        #  "../os-java-projects/commons-lang__master__https://github.com/apache/commons-lang/commit/__io/artifacts/commons-lang__commons-lang__step3__commons-lang.json"
        #  "../os-java-projects/joda-time__main__https://github.com/JodaOrg/joda-time/commit/__io/artifacts/joda-time__joda-time__step3__joda-time.json__true"
        #  "../os-java-projects/pmd__master__https://github.com/pmd/pmd/commit/__io/artifacts/pmd__pmd__step3__pmd.json__true"
        #  "../os-java-projects/gson__master__https://github.com/google/gson/commit/__io/artifacts/gson__gson__step3__gson.json__true"
        #  "../os-java-projects/commons-math__master__https://github.com/apache/commons-math/commit/__io/artifacts/commons-math__commons-math__step3__commons-math.json__true"
        #  "../os-java-projects/jfreechart__master__https://github.com/jfree/jfreechart/commit/__io/artifacts/jfreechart__jfreechart__step3__jfreechart.json__true"
        #  "../os-java-projects/cts__master__https://android.googlesource.com/platform/cts/+/__io/artifacts/cts__cts__step3__cts.json__true"
             )

for project_data in "${projects[@]}"
do
    set -f # avoid globbing (expansion of *).
    project_arr=(${project_data//__/ }) # ${string//substring/replacement}
#    for j in "${!project_arr[@]}" # converts into array of index 0, 1
#    do
#      echo "${date_arr[j]}"
#    done
    REPO_PATH="${project_arr[0]}"  TARGET_BRANCH="${project_arr[1]}" COMMIT_BASE_URL="${project_arr[2]}" COMMIT_START_DATE="01/01/2000" COMMIT_END_DATE="01/01/2023" OUTPUT_DIR="${project_arr[3]}" PROJECT="${project_arr[4]}" STEP="${project_arr[5]}" REFACTOR_FILE="${project_arr[6]}" HANDLE_EXPORT="true" nohup python3 main.py &
done
