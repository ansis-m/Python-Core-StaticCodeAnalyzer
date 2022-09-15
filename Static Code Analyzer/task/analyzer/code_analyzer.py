"""
Module's docstring.
"""

import os
import sys
import re
import ast

S001 = ": Line {}: S001 Too long"
S002 = ": Line {}: S002 Indentation is not a multiple of four"
S003 = ": Line {}: S003 Unnecessary semicolon"
S004 = ": Line {}: S004 At least two spaces required before inline comments"
S005 = ": Line {}: S005 TODO found"
S006 = ": Line {}: S006 More than two blank lines used before this line"
S007 = ": Line {}: S007 Too many spaces after construction_name (def or class)"
S008 = ": Line {}: S008 Class name class_name should be written in CamelCase"
S009 = ": Line {}: S009 Function name function_name should be written in snake_case"
S010 = ": Line {}: S010 Argument name arg_name should be written in snake_case"
S011 = ": Line {}: S011 Variable var_name should be written in snake_case"
S012 = ": Line {}: S012 The default argument value is mutable"


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


def many_spaces_after_construction_name(line):
    ''''make sure just one space after the constructor'''
    temp = line.strip()

    if re.match('class ', temp) and re.match('class  ', temp):
        return True
    if re.match('def ', temp) and re.match('def  ', temp):
        return True

    return False


def bad_class_name(line):
    ''''make sure class name is camel case'''

    temp = line.strip()
    if re.match('class ', temp):
        class_name = re.split(":|\(", temp[5::].strip())[0]
        if not re.match("^([A-Z][a-z0-9]+)+$", class_name):
            return True

    return False


def bad_function_name(line):
    ''''make sure function name is snake case'''
    temp = line.strip()
    if re.match('def ', temp):
        function_name = re.split("\(", temp[3::].strip())[0]
        function_name = function_name.strip("__")

        if not re.match("^[a-z][a-z0-9]+(_[a-z][a-z0-9]+)*$", function_name):
            return True

    return False


def check(line, index, filename):
    ''''run all the checks on current line'''

    errors = []

    if too_long(line):
        errors.append(filename + S001.format(index))
    if bad_indentation(line):
        errors.append(filename + S002.format(index))
    if unnecessary_semicolon(line):
        errors.append(filename + S003.format(index))
    if missing_spaces(line):
        errors.append(filename + S004.format(index))
    if todo_found(line):
        errors.append(filename + S005.format(index))
    if many_spaces_after_construction_name(line):
        errors.append(filename + S007.format(index))
    if bad_class_name(line):
        errors.append(filename + S008.format(index))
    if bad_function_name(line):
        errors.append(filename + S009.format(index))

    return errors


def check_file(filename):
    '''Manager-Function to check each file. All input and output is logged in logfile.txt and output.txt'''
    log = open("logfile.txt", "a", encoding="utf-8")
    output = open("output.txt", "a", encoding="utf-8")
    ast_log = open("ast.txt", "a", encoding="utf-8")

    output.write("*************************************\n")
    log.write("*************************************\n")
    errors = []
    with open(filename, "r", encoding="utf-8") as file:
        empty_lines = 0
        for index, line in enumerate(file, start=1):
            log.write("{}: ".format(index) + line)
            errors += check(line, index, filename)
            if not blank(line):
                if empty_lines > 2:
                    errors.append(filename + S006.format(index))
                empty_lines = 0
            else:
                empty_lines += 1


        # AST MODULE BEGIN
        file.seek(0)
        tree = ast.parse(file.read())
        nodes = ast.walk(tree)
        ast_log.write("***********************FILE***********************\n")
        for indx, node in enumerate(nodes, start=1):
            ast_log.write(f"node no {indx}: ")
            ast_log.write(f"dump {node}\n")
            if not isinstance(node, ast.Module):
                # ast_log.write("_________________node_________________\n")
                # ast_log.write("node.lineno: {}\n".format(node.lineno))
                # ast_log.write("node.col_offset: {}\n".format(node.col_offset))
                # ast_log.write("isinstance(node, ast.FunctionDef): {}\n".format(isinstance(node, ast.FunctionDef)))
                # ast_log.write("isinstance(node, ast.Name): {}\n".format(isinstance(node, ast.Name)))
                if isinstance(node, ast.FunctionDef):
                    args = [a.arg for a in node.args.args]
                    ast_log.write("\n\t....function args....\n")
                    for arg in args:
                        ast_log.write(f"\t{arg}\n")
                    ast_log.write("\n\t....function args end....\n")





        # AST MODULE END
        #errors.sort()
        for error in errors:
            output.write(error + "\n")
            print(error)

    output.close()
    log.close()
    ast_log.close()


def main():
    '''Main function of the programm'''

    if os.path.exists("logfile.txt"):
        os.remove("logfile.txt")
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    if os.path.exists("ast.txt"):
        os.remove("ast.txt")

    if os.path.isfile(sys.argv[1]):
        check_file(sys.argv[1])
    elif os.path.isdir(sys.argv[1]):
        contents = os.listdir(sys.argv[1])
        contents.sort()
        for file in contents:
            if file.endswith(".py"):
                check_file(sys.argv[1] + "\\" + file)


if __name__ == "__main__":
    main()
