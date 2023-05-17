from enum import Enum


class Pattern(str, Enum):
    # Define useful regular patterns
    TEST_FILENAME = "^(.*)Test(.*).java$"
    REMOVED_TEST_ANNOTATION = "-([ \t]*)@(.*)Test"
    REMOVED_TEST_FUNCTION_PROTOTYPE = "-([ \t]*)(public)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)test([a-zA-Z0-9_]+)" \
                                      "([ \t]*)\\("
    REMOVED_TEST_FUNCTION_PROTOTYPE2 = "-([ \t]*)@Test(.*?)([ \t\n\r]*)(-([ \t]*)@(.*?)([ \t\n\r]*))*-([ \t]*)(public)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)([a-zA-Z0-9_]+)" \
                                      "([ \t]*)\\("
    REFACTORED_TEST_FUNCTION_PROTOTYPE = "-([ \t]*)(public)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)test([a-zA-Z0-9_]+)" \
                                            "([ \t]*)\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)([ \t\n\r]*)([a-zA-Z0-9_ ,\\-\t\n\r]*)\\{" \
                                            "([a-zA-Z0-9_ ,\\-\t\n\r]*)\\+"
    REFACTORED_TEST_FUNCTION_PROTOTYPE2 = "-([ \t]*)@Test(.*?)([ \t\n\r]*)(-([ \t]*)@(.*?)([ \t\n\r]*))*-([ \t]*)(public)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)([a-zA-Z0-9_]+)" \
                                      "([ \t]*)\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)([ \t\n\r]*)([a-zA-Z0-9_ ,\\-\t\n\r]*)\\{" \
                                    "([a-zA-Z0-9_ ,\\-\t\n\r]*)\\+"
    ADDED_TEST_FUNCTION_PROTOTYPE = "\\+([ \t]*)(public)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)test([a-zA-Z0-9_]+)" \
                                    "([ \t]*)\\("
    ADDED_TEST_FUNCTION_PROTOTYPE2 = "\\+([ \t]*)@Test(.*?)([ \t\n\r]*)(\\+([ \t]*)@(.*?)([ \t\n\r]*))*\\+([ \t]*)(public)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)([a-zA-Z0-9_]+)" \
                                      "([ \t]*)\\("                                
    REMOVED_ASSERT_FUNCTION_PROTOTYPE = "-([ \t]*)assert([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \t\n]*\\)"
    FUNCTION_NAME_AND_SIGNATURE = "([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)"
    FUNCTION_NAME = "([a-zA-Z0-9_]+)([ \t]*)\\("
    FUNCTION_ARGUMENTS = "\\(.*\\)"
