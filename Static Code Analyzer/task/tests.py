from hstest.stage_test import *
from hstest.test_case import TestCase
from re import search
import os

TOO_LONG_LINE = 'Too long line is not mentioned'
INDENTATION = "Invalid check of indentation (S002). "
UNNECESSARY_SEMICOLON = "Your program passed the line with an unnecessary semicolon or has an incorrect format. "
FALSE_ALARM = "False alarm. Your program warned about correct row. "
TODO = "Your program passed the line with TODO comment or has an incorrect format. "
TOO_MANY_BLANK_LINES = "Your program didn't warn about more than two blank lines between lines."
TWO_SPACES_BEFORE_COMMENT = "The program should warn about the line with less than 2 spaces before a comment."
INCORRECT_LINE_ORDER = "Your program did not sort correctly the errors according to the numbers of code lines."
INCORRECT_ERRORS_ORDER = "Your program did not sort correctly the errors according to the error codes."
INCORRECT_FORMAT = "Your program does not seem to output error message in the correct format in the following line: \n" \
                   "\"{0}\"\n" \
                   "Make sure you output the words \"Line N\", where N is the number of the line, \n" \
                   "a semicolon and the code of the error."


class AnalyzerTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [TestCase(stdin=f"test{os.sep}test_0.py", attach=0),
                TestCase(stdin=f"test{os.sep}test_1.py", attach=1),
                TestCase(stdin=f"test{os.sep}test_2.py", attach=2),
                TestCase(stdin=f"test{os.sep}test_3.py", attach=3),
                TestCase(stdin=f"test{os.sep}test_4.py", attach=4),
                TestCase(stdin=f"test{os.sep}test_5.py", attach=5),
                TestCase(stdin=f"test{os.sep}test_6.py", attach=6)]

    # Check the correct order of lines and errors
    def test_0(self, output: str):
        output_split = output.strip().splitlines()
        output_formatted = output.lower().strip().splitlines()
        line_numbers = []
        errors = []
        for i, line in enumerate(output_formatted):
            template = r'line (\d+): ?s00(\d)'
            match = search(template, line)
            if not match:
                return CheckResult.wrong(INCORRECT_FORMAT.format(output_split[i]))
            line_numbers.append(int(match.group(1)))
            errors.append(int(match.group(2)))
        line_order_errors = [int(not line_n <= line_numbers[i + 1])
                             if i + 1 != len(line_numbers) else 0
                             for i, line_n in enumerate(line_numbers)]
        if sum(line_order_errors) > 0:
            return CheckResult.wrong(INCORRECT_LINE_ORDER)

        order_errors = [int(not error < errors[i + 1])
                        if i + 1 != len(errors) and line_numbers[i] == line_numbers[i + 1]
                        else 0
                        for i, error in enumerate(errors)]
        if sum(order_errors) > 0:
            return CheckResult.wrong(INCORRECT_ERRORS_ORDER)

        return CheckResult.correct()

    # Check of indention violation
    def test_1(self, output: str):
        error_code = "s002"
        output = output.strip().lower().splitlines()
        if not len(output) == 3:
            return CheckResult.wrong("Incorrect number of warning messages. "
                                     "Your program should warn about 3 lines with mistakes.\n"
                                     "Choose only those lines where indentation is not a multiple of four.")
        if not output[0].startswith(f"line 2: {error_code}"):
            return CheckResult.wrong(INDENTATION + "Your program passed the row with single column indent.")
        if not output[1].startswith(f"line 3: {error_code}"):
            return CheckResult.wrong(INDENTATION + "Your program passed the row with two columns indent.")
        if not output[2].startswith(f"line 5: {error_code}"):
            return CheckResult.wrong(INDENTATION + "Your program passed the row with six columns indent.")
        return CheckResult.correct()

    # Test of semicolon violation
    def test_2(self, output: str):
        error_code = "s003"
        output = output.strip().lower().splitlines()
        if not output:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        # negative tests
        for item in output:
            if item.startswith(f"line 1: {error_code}"):
                return CheckResult.wrong(FALSE_ALARM + "There was no any semicolons at all.")
            if item.startswith(f"line 5: {error_code}") or item.startswith(f"line 8 {error_code}"):
                return CheckResult.wrong(FALSE_ALARM + "The semicolon was a part of comment block")
            if item.startswith(f"line 6: {error_code}") or item.startswith(f"line 7 {error_code}"):
                return CheckResult.wrong(FALSE_ALARM + "The semicolon was a part of string")

        # positive tests
        if not len(output) == 3:
            return CheckResult.wrong("Incorrect number of warning messages.")
        for i, j in enumerate([2, 3, 4]):
            if not output[i].startswith(f"line {j}: {error_code}"):
                return CheckResult.wrong(UNNECESSARY_SEMICOLON)
        return CheckResult.correct()

    # Test of todo_comments
    def test_3(self, output: str):
        error_code = "s005"
        output = output.strip().lower().splitlines()
        if not output:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        # negative tests
        for item in output:
            if item.startswith(f"line 1: {error_code}") or item.startswith(f"line 8 {error_code}") or \
                    item.startswith(f"line 9: {error_code}"):
                return CheckResult.wrong(FALSE_ALARM + "There was no any TODO comments")
            if item.startswith(f"line 6: {error_code}") or item.startswith(f"line 7 {error_code}"):
                return CheckResult.wrong(FALSE_ALARM + "TODO is inside of string")

        # positive tests
        if not len(output) == 4:
            return CheckResult.wrong("A wrong number of warning messages. "
                                     "Your program should warn about 4 lines with mistakes in this test case.\n"
                                     "4 lines that include TODO comments should be found")
        for i, j in enumerate([2, 3, 4, 5]):
            if not output[i].startswith(f"line {j}: {error_code}"):
                return CheckResult.wrong(TODO)

        return CheckResult.correct()

    # Blank lines test
    def test_4(self, output):
        error_code = "s006"
        output = output.strip().lower()
        if len(output) < 1:
            return CheckResult.wrong("The program's output is empty. One error message was expected.")
        output = output.splitlines()
        if len(output) != 1:
            if output[0].startswith(f"line 4: {error_code}"):
                return CheckResult.wrong(FALSE_ALARM)
            if not output[0].startswith(f"line 8: {error_code}"):
                return CheckResult.wrong(TOO_MANY_BLANK_LINES)
            else:
                return CheckResult.wrong(TOO_MANY_BLANK_LINES)
        return CheckResult.correct()

    # Test of comments style
    def test_5(self, output):
        error_code = "s004"
        output = output.strip().lower().splitlines()
        if not output:
            return CheckResult.wrong("It looks like there is no messages from your program.")

        # negative tests
        for item in output:
            if item.startswith(f"line 1: {error_code}"):
                return CheckResult.wrong(FALSE_ALARM + "There is no comments at all.")
            if item.startswith(f"line 2: {error_code}"):
                return CheckResult.wrong(FALSE_ALARM + "There is a correct line with comment")
            if item.startswith(f"line 3: {error_code}" or item.startswith(f"line 4: {error_code}")):
                return CheckResult.wrong(FALSE_ALARM + "It is a correct line with a comment after code.")

        # positive test
        for i, j in enumerate([6, 7]):
            if not output[i].startswith(f"line {j}: {error_code}"):
                return CheckResult.wrong(TWO_SPACES_BEFORE_COMMENT)

        return CheckResult.correct()

    def test_6(self, output):
        output = output.strip().lower().splitlines()

        if len(output) != 9:
            return CheckResult.wrong("It looks like there is an incorrect number of error messages. "
                                     f"Expected 9 lines, found {len(output)}")

        if not (output[0].startswith("line 1: s004") or
                output[7].startswith("line 13: s004")):
            return CheckResult.wrong(TWO_SPACES_BEFORE_COMMENT)

        if not (output[1].startswith("line 2: s003") or
                output[3].startswith("line 3: s003") or
                output[6].startswith("line 13: s003")):
            return CheckResult.wrong(UNNECESSARY_SEMICOLON)

        if not (output[2].startswith("line 3: s001") or
                output[4].startswith("line 6: s001")):
            return CheckResult.wrong(TOO_LONG_LINE)

        if not (output[5].startswith("line 11: s006")):
            return CheckResult.wrong(TOO_MANY_BLANK_LINES)

        if not output[8].startswith("line 13: s005"):
            return CheckResult.wrong(TODO)

        return CheckResult.correct()

    def check(self, reply: str, attach) -> CheckResult:
        if attach == 0:
            output = self.test_0(reply)
        elif attach == 1:
            output = self.test_1(reply)
        elif attach == 2:
            output = self.test_2(reply)
        elif attach == 3:
            output = self.test_3(reply)
        elif attach == 4:
            output = self.test_4(reply)
        elif attach == 5:
            output = self.test_5(reply)
        elif attach == 6:
            output = self.test_6(reply)
        else:
            return CheckResult.wrong("Unknown error")

        return output


if __name__ == '__main__':
    AnalyzerTest("analyzer.code_analyzer").run_tests()
