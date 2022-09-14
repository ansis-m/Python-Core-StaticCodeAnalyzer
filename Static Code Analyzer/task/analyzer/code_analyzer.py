"""
Module's docstring.
"""

def main():
    '''Main function of the programm'''
    filename = input()
    with open(filename, "r", encoding="utf-8") as file:
        for index, line in enumerate(file):
            if len(line) > 79:
                print(f"Line {index + 1}: S001 Too long")

if __name__ == "__main__":
    main()
