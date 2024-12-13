import argparse
import sys
import re
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

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
    st = []
    for line in lines:
        if line:
            st.append(line)
        else:
            res.append(st)
            st = []
    if st:
        res.append(st)
    games = []
    for game in res:
        btna = re.findall(r'(\d+)', game[0])
        btnb = re.findall(r'(\d+)', game[1])
        total = re.findall(r'(\d+)', game[2])
        btna = list(map(int, btna))
        btnb = list(map(int, btnb))
        total = list(map(int, total))
        games.append((btna, btnb, total))
    return games


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    ans = 0
    for game in data:
        coef = (game[2][0] // game[0][0]) + 1
        total = [coef * game[0][0], coef * game[0][1]]
        tokens = [coef * 3, 0]
        if game[2][1] - total[1] > 0:
            coef = ((game[2][1] - total[1]) // game[0][1]) + 1
        while tokens[0] > 0:
            total[0] -= game[0][0]
            total[1] -= game[0][1]
            tokens[0] -= 3
            while total[0] < game[2][0] or total[1] < game[2][1]:
                tokens[1] += 1
                total[0] += game[1][0]
                total[1] += game[1][1]
            if total[0] == game[2][0] and total[1] == game[2][1]:
                if tokens[0] < 300 and tokens[1] < 100:
                    ans += sum(tokens)
                break

    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)


    return 0


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
