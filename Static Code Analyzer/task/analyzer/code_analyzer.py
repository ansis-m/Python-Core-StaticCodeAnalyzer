"""
Module's docstring.
"""

import os
import sys

LONG = ": Line {}: S001 Too long"
INDENTATION = ": Line {}: S002 Indentation is not a multiple of four"
SEMICOLON = ": Line {}: S003 Unnecessary semicolon"
BLANK_LINES = ": Line {}: S006 More than two blank lines used before this line"
TODO = ": Line {}: S005 TODO found"
SPACES = ": Line {}: S004 At least two spaces required before inline comments"

def too_long(line):
    '''Check if line is longer than 79 chars'''
    return len(line) > 79

def missing_spaces(line):
    '''Check if there are at least two spaces before the inline comment'''
    for index, char in enumerate(line):
        if char == '#':
            if index > 1 and (line[index - 1] != ' ' or line[index - 2] != ' '):
                return True
            else:
                return False
    return False

def blank(line):
    '''Check if line is blank'''
    return len(line.strip()) == 0

def bad_indentation(line):
    '''check if leading spaces % 4 == 0'''
    indentation = 0

    for char in line:
        if char == ' ':
            indentation += 1
        else:
            break

    return indentation % 4 != 0

def todo_found(line):
    '''check if there is todo in comments'''

    uc_line = line.upper()

    for index, char in enumerate(line):
        if char == '#':
            if uc_line.find("TODO", index, -1) > -1:
                return True

    return False


def unnecessary_semicolon(line):
    '''check if there is unnecessary_semicolon'''
    quotes = 0
    double_quotes = 0

    for char in line:
        if char == "#":
            return False
        if char == "\"":
            double_quotes += 1
        elif char == "\'":
            quotes += 1
        elif char == ";" and not (quotes % 2 or double_quotes % 2):
            return True
    return False


def check(line, index, filename):
    ''''run all the checks on current line'''

    errors = []

    if too_long(line):
        errors.append(filename + LONG.format(index))
    if bad_indentation(line):
        errors.append(filename + INDENTATION.format(index))
    if unnecessary_semicolon(line):
        errors.append(filename + SEMICOLON.format(index))
    if missing_spaces(line):
        errors.append(filename + SPACES.format(index))
    if todo_found(line):
        errors.append(filename + TODO.format(index))

    return errors


def check_file(filename):

    log = open("logfile.txt", "a", encoding="utf-8")
    output = open("output.txt", "a", encoding="utf-8")
    with open(filename, "r", encoding="utf-8") as file:
        empty_lines = 0
        for index, line in enumerate(file, start=1):
            log.write(line)
            errors = check(line, index, filename)
            if not blank(line):
                if empty_lines > 2:
                    errors.append(filename + BLANK_LINES.format(index))
                empty_lines = 0
            else:
                empty_lines += 1
            errors.sort()
            for error in errors:
                output.write(error + "\n")
                print(error)

    output.close()
    log.close()



def main():
    '''Main function of the programm'''

    if os.path.exists("logfile.txt"):
        os.remove("logfile.txt")
    if os.path.exists("output.txt"):
        os.remove("output.txt")

    filename = sys.argv[1]
    if os.path.isfile(filename):
        check_file(filename)
    elif os.path.isdir(filename):

        pass# print("filename:", filename)




if __name__ == "__main__":
    main()
