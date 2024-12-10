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
        res.append(line)
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    def dfs(row, col, iter) -> list:
        if 0 <= row < len(data) and 0 <= col < len(data[0]) and data[row][col] == f'{iter}':
            if seen[row][col]:
                return []
            seen[row][col] = True
            if iter == 9:
                if data[row][col] == '9':
                    return [[row, col]]
                return []
            res = []
            for rr, cc in direction:
                res += dfs(row + rr, col + cc, iter + 1)
            return res
        return []


    data = parse_data(lines)
    direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    ans = 0

    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == '0':
                seen = [[False for _ in range(len(data[0]))] for _ in range(len(data))]
                ans += len(dfs(row, col, 0))
    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def dfs(row, col, iter) -> list:
        if 0 <= row < len(data) and 0 <= col < len(data[0]) and data[row][col] == f'{iter}':
            if iter == 9:
                if data[row][col] == '9':
                    return [[row, col]]
                return []
            res = []
            for rr, cc in direction:
                res += dfs(row + rr, col + cc, iter + 1)
            return res
        return []


    data = parse_data(lines)
    direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    ans = 0

    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == '0':
                ans += len(dfs(row, col, 0))
    return ans


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
