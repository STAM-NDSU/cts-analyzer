from enum import Enum


class Pattern(str, Enum):
    # Define useful regular patterns
    TEST_FILENAME = "^.*Test.java$|^Test(.*).java$"
    REMOVED_TEST_ANNOTATION = "-([ \t]*)@(.*)Test"
    REMOVED_TEST_FUNCTION_PROTOTYPE = "-([ \t]*)(public|private|protected)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)test([a-zA-Z0-9_]+)" \
                                      "([ \t]*)\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)([ \t]*)([a-zA-Z0-9_ ,\\-\n\\t]*)\\{"
    REMOVED_TEST_FUNCTION_PROTOTYPE2 = "-([ \t]*)@Test([- \n]*)-([ \t]*)(public|private|protected)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)([a-zA-Z0-9_]+)" \
                                      " *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)([ \t]*)([a-zA-Z0-9_ ,\\-\n]*)([ \t]*)\\{"
    REFACTORED_TEST_FUNCTION_PROTOTYPE = "-([ \t]*)(public|private|protected)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)test([a-zA-Z0-9_]+)" \
                                            "([ \t]*)\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)([ \t]*)([a-zA-Z0-9_ ,\\-\n]*)([ \t]*)\\{([- \t\n]*)" \
                                            "\\+"
    ADDED_TEST_FUNCTION_PROTOTYPE = "\\+([ \t]*)(public|private|protected)([ \t]*)([a-zA-Z0-9<>._?, ]+)([ \t]*)test([a-zA-Z0-9_]+)" \
                                    "([ \t]*)\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)([ \t]*)([a-zA-Z0-9_ ,\n\\+]*)([ \t]*)\\{"
    REMOVED_ASSERT_FUNCTION_PROTOTYPE = "-([ \t]*)assert([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)"
    FUNCTION_NAME_AND_SIGNATURE = "([a-zA-Z0-9_]+) *\\([a-zA-Z0-9<>\\[\\]._?, \n]*\\)"
    FUNCTION_NAME = "([a-zA-Z0-9_]+) *\\("
    FUNCTION_ARGUMENTS = "\\(.*\\)"
