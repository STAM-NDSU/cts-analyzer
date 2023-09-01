from enum import Enum


class Pattern(str, Enum):
    # Define useful regular patterns
    JAVA_FILENAME = "*.java" 
    # TEST_FILENAME = "^(.*)Test(.*).java$" # contains Test in the filename
    TEST_FILENAME = "^Test(.*).java$|(.*)Test.java"  # contains Test at the beginning or at the end in the filename
    TEST_FUNCTION_PROTOTYPE = (
        "([ \t]*)(public)([ \t\n\r]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r]*)test([a-zA-Z0-9_]+)"
        "([ \t\n\r]*)\\("
    )
    TEST_FUNCTION_PROTOTYPE2 = (
        "([ \t]*)@Test(.*?)([ \t\n\r]*)(([ \t]*)@(.*?)([ \t\n\r]*))*([ \t]*)(public)([ \t\n\r]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\-]*)([a-zA-Z0-9_]+)"
        "([ \t\n\r]*)\\("
    )
    REMOVED_TEST_ANNOTATION = "-([ \t]*)@(.*)Test"
    REMOVED_TEST_FUNCTION_PROTOTYPE = (
        "-([ \t]*)(public)([ \t\n\r\\-]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\-]*)test([a-zA-Z0-9_]+)"
        "([ \t\n\r\\-]*)\\("
    )
    REMOVED_TEST_FUNCTION_PROTOTYPE2 = (
        "-([ \t]*)@Test(.*?)([ \t\n\r]*)(-([ \t]*)@(.*?)([ \t\n\r]*))*-([ \t]*)(public)([ \t\n\r\\-]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\-]*)([a-zA-Z0-9_]+)"
        "([ \t\n\r\\-]*)\\("
    )
    REFACTORED_TEST_FUNCTION_PROTOTYPE = (
        "-([ \t]*)(public)([ \t\n\r\\-]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\-]*)test([a-zA-Z0-9_]+)"
        "([ \t\n\r\\-]*)\\([a-zA-Z0-9<>\\[\\]._?, \t\n\r\\-]*\\)([ \t\n\r\\-]*)([a-zA-Z0-9_ ,\\-\t\n\r]*)\\{?"
        "([a-zA-Z0-9_ ,\\-\t\n\r]*)\\+"
    )
    REFACTORED_TEST_FUNCTION_PROTOTYPE2 = (
        "-([ \t]*)@Test(.*?)([ \t\n\r]*)(-([ \t\n\r]*)@(.*?)([ \t\n\r]*))*-([ \t]*)(public)([ \t\n\r\\-]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\-]*)([a-zA-Z0-9_]+)"
        "([ \t\n\r\\-]*)\\([a-zA-Z0-9<>\\[\\]._?, \t\n\r]*\\)([ \t\n\r\\-]*)([a-zA-Z0-9_ ,\\-\t\n\r]*)\\{?"
        "([a-zA-Z0-9_ ,\\-\t\n\r]*)\\+"
    )
    ADDED_TEST_FUNCTION_PROTOTYPE = (
        "\\+([ \t]*)(public)([ \t\n\r\\+]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\+]*)test([a-zA-Z0-9_]+)"
        "([ \t\n\r\\+]*)\\("
    )
    ADDED_TEST_FUNCTION_PROTOTYPE2 = (
        "\\+([ \t\n\r]*)@Test(.*?)([ \t\n\r]*)(\\+([ \t]*)@(.*?)([ \t\n\r]*))*\\+([ \t]*)(public)([ \t\n\r\\+]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\+]*)([a-zA-Z0-9_]+)"
        "([ \t\n\r\\+]*)\\("
    )
    REMOVED_ASSERT_FUNCTION_PROTOTYPE = (
        "-([ \t]*)assert([a-zA-Z0-9_]+)([ \t\n\r\\-]*)\\("
    )
    FUNCTION_NAME_AND_SIGNATURE = "([a-zA-Z0-9_]+)[ \t\n\r]*)([a-zA-Z0-9<>\\[\\]._?, \t\n\r\\+\\-]*\\)"  # can be for both added/deleted testcases
    TEST_FUNCTION_NAME_WITH_SPACE_BEFORE = " test([a-zA-Z0-9_]+)([ \t]*)\\("
    TEST_FUNCTION_NAME = "test([a-zA-Z0-9_]+)([ \t]*)\\("
    FUNCTION_NAME_WITH_SPACE_BEFORE = " ([a-zA-Z0-9_]+)([ \t]*)\\("  # QUICK FIX FOR mutilple annotations before testcase issue
    FUNCTION_NAME = "([a-zA-Z0-9_]+)([ \t]*)\\("
    # FUNCTION_NAME = "(?<!@)([a-zA-Z0-9_]+)([ \t]*)\\("
    FUNCTION_ARGUMENTS = "\\(.*\\)"
    CHANGE_ID = "Change-Id: ([a-zA-Z0-9]{41})"
    BUG_ID = "bug(: )*([0-9]{5,15})"
