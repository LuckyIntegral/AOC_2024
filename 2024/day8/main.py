import argparse
import os


INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')

def content() -> list[str]:
    '''Reads the input file and returns a list of strings'''
    def read_file(file: str) -> list[str]:
        if not os.path.exists(file):
            print(f"File {file} not found")
            exit(1)
        with open(file) as f:
            lines = f.readlines()
        return [line.strip() for line in lines]

    return read_file(INPUT_FILE), read_file(TEST_FILE)


def parse_data(lines: list[str]) -> any:
    '''Parses the data'''
    res = []
    for line in lines:
        res.append(list(line))
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    from collections import defaultdict
    points = defaultdict(list)

    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char != ".":
                points[char].append((row, col))

    for v in points.values():
        for i in range(len(v) - 1):
            for j in range(i + 1, len(v)):
                drow, dcol = v[i][0] - v[j][0], v[i][1] - v[j][1]
                l, r = [v[i][0] + drow, v[i][1] + dcol], [v[j][0] - drow, v[j][1] - dcol]
                if 0 <= l[0] < len(data) and 0 <= l[1] < len(data[0]):
                    data[l[0]][l[1]] = "#"
                if 0 <= r[0] < len(data) and 0 <= r[1] < len(data[0]):
                    data[r[0]][r[1]] = "#"

    return sum(1 for line in data for char in line if char == "#")


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    from collections import defaultdict
    points = defaultdict(list)

    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char != ".":
                points[char].append((row, col))

    for v in points.values():
        for i in range(len(v) - 1):
            for j in range(i + 1, len(v)):
                drow, dcol = v[i][0] - v[j][0], v[i][1] - v[j][1]
                l, r = [v[i][0] + drow, v[i][1] + dcol], [v[j][0] - drow, v[j][1] - dcol]
                while 0 <= l[0] < len(data) and 0 <= l[1] < len(data[0]):
                    if data[l[0]][l[1]] == ".":
                        data[l[0]][l[1]] = "#"
                    l[0] += drow
                    l[1] += dcol
                while 0 <= r[0] < len(data) and 0 <= r[1] < len(data[0]):
                    if data[r[0]][r[1]] == ".":
                        data[r[0]][r[1]] = "#"
                    r[0] -= drow
                    r[1] -= dcol

    return sum(1 for line in data for char in line if char != ".")


def parse_args():
    '''Parses the arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        help="run the test samples only",
        action="store_true"
    )
    return parser.parse_args()


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    options = parse_args()
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    if options.debug:
        return
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
