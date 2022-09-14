def main():
    filename = input()
    file = open(filename, "r")
    for index, line in enumerate(file):
        if len(line) > 79:
            print("Line {}: S001 Too long".format(index + 1))


if __name__ == "__main__":
    main()
