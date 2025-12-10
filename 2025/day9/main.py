import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    return content.splitlines()


from itertools import combinations
def silver(content: str):
    '''Solves the silver problem'''
    data = parse_data(content)
    dots = []
    for line in data:
        x, y = map(int, line.split(','))
        dots.append((x, y))

    squares = [(abs(x1 - x2) + 1) * (abs(y1 - y2) + 1) for (x1, y1), (x2, y2) in combinations(dots, 2)]
    return max(squares)

from collections import defaultdict
def gold(content: str):
    '''Solves the gold problem'''
    data = parse_data(content)
    dots = []
    hshX = defaultdict(list)
    hshY = defaultdict(list)

    for line in data:
        x, y = map(int, line.split(','))
        hshX[x].append(y)
        hshY[y].append(x)
        dots.append((x, y))

    res = 0

    for (x1, y1), (x2, y2) in combinations(dots, 2):
        minx, maxx = min(x1, x2), max(x1, x2)
        miny, maxy = min(y1, y2), max(y1, y2)
        valid = True

        for y in range(miny + 1, maxy):
            if not hshY[y]:
                continue
            ax, bx = hshY[y]
            if not (max(ax, bx) <= minx or maxx <= min(ax, bx)):
                valid = False
                break
        if not valid:
            continue

        for x in range(minx + 1, maxx):
            if not hshX[x]:
                continue
            ay, by = hshX[x]
            if not (max(ay, by) <= miny or maxy <= min(ay, by)):
                valid = False
                break
        if not valid:
            continue

        res = max(res, (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1))

    return res


def main():
    '''Parses the input and solves the two problems'''
    options = lib.parse_args()

    content = lib.read_file(TEST_FILE)
    print(f"Silver test: {silver(content)}")
    print(f"Gold test:   {gold(content)}")

    if not options.debug:
        content = lib.read_file(INPUT_FILE)
        print(f"Silver:      {silver(content)}")
        print(f"Gold:        {gold(content)}")


if __name__ == "__main__":
    main()
