"""
Module's docstring.
"""

def too_long(line):
    '''Check if line is longer than 79 chars'''
    return len(line) > 79

def missing_spaces(line):
    '''check if there are at least two spaces before the inline comment'''
    for index, char in enumerate(line):
        if char == "#" and index > 1 and (line[index - 1] != ' ' or line[index - 2] != ' '):
            return True
    return False

def blank(line):
    return len(line.strip()) == 0

def bad_indentation(line):
    indentation = 0

    for char in line:
        if char == ' ':
            indentation += 1
        else:
            break

    return indentation % 4 == 0

def missing_spaces(line):
    pass

def todo_found(line):
    pass

def unnecessary_semicolon(line):
    pass


def check(line, index):

    result = list()

    if too_long(line):
        errors.append(f"Line {index + 1}: S001 Too long")
    if bad_indentation(line):
        errors.append(f"Line {index + 1}: S002 Indentation is not a multiple of four")
    if unnecessary_semicolon(line):
            errors.append(f"Line {index + 1}: S003 Unnecessary semicolon")
    if missing_spaces(line):
        errors.append(f"Line {index + 1}: S004 At least two spaces required before inline comments")
    if todo_found(line):
        errors.append(f"Line {index + 1}: S005 TODO found")

    return result


def main():
    '''Main function of the programm'''
    filename = input()
    with open(filename, "r", encoding="utf-8") as file:
        empty_lines = 0
        for index, line in enumerate(file):
            errors = check(line, index)
            if not blank(line):
                if empty_lines > 2:
                    errors.append(f"Line {index + 1}: S006 More than two blank lines used before this line")
                empty_lines = 0
            else:
                empty_lines += 1
            errors.sort()
            for error in errors:
                print(error)

if __name__ == "__main__":
    main()
