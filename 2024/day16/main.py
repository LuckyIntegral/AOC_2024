import argparse
import sys
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
    for line in lines:
        res.append(line)
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    start = lib.grid_find(data, 'S')
    finish = lib.grid_find(data, 'E')
    visited = [[False for _ in range(len(data[0]))] for _ in range(len(data))]
    queue = [(start, 0, 'U')]
    directions = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }

    while queue:
        (x, y), steps, dr = queue.pop(0)
        if visited[x][y] or data[x][y] == '#':
            continue
        visited[x][y] = True
        if (x, y) == finish:
            return steps + 1000 # small feature
        for k, v in directions.items():
            if k == dr:
                queue.append(((x + v[0], y + v[1]), steps + 1, k))
            else:
                queue.append(((x + v[0], y + v[1]), steps + 1001, k))
        queue = sorted(queue, key=lambda x: x[1])

    return -1


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def after_corners(data, path):
        corners = set()
        prev = path[0][-1]
        for (x, y, d) in path:
            if d != prev:
                corners.add((x, y))
            prev = d
        return corners
    data = parse_data(lines)
    start = lib.grid_find(data, 'S')
    finish = lib.grid_find(data, 'E')
    visited = [[False for _ in range(len(data[0]))] for _ in range(len(data))]
    queue = [(start, 1000, 'U', [[start[0], start[1], 'U']])]
    directions = {
        'U': (-1, 0),
        'R': (0, 1),
        'D': (1, 0),
        'L': (0, -1)
    }
    opposite = {
        'U': 'D',
        'D': 'U',
        'L': 'R',
        'R': 'L'
    }
    pathes = []
    best_cost = -1

    while queue:
        (x, y), steps, dr, path = queue.pop(0)
        if visited[x][y] or data[x][y] == '#':
            continue
        visited[x][y] = True
        if (x, y) == finish:
            best_cost = steps
            pathes.append(path)
            break
        for k, v in directions.items():
            if k == dr:
                queue.append(((x + v[0], y + v[1]), steps + 1, k, path + [[x + v[0], y + v[1], k]]))
            elif k != opposite[dr]:
                queue.append(((x + v[0], y + v[1]), steps + 1001, k, path + [[x + v[0], y + v[1], k]]))
        queue = sorted(queue, key=lambda x: x[1])

    corners = after_corners(data, path)
    seen = set()
    data = [list(row) for row in data]
    i = 0
    while corners:
        xx, yy = corners.pop()
        if (xx, yy) in seen:
            continue

        seen.add((xx, yy))
        visited = [[False for _ in range(len(data[0]))] for _ in range(len(data))]
        data[xx][yy] = '#'
        queue = [(start, 1000, 'U', [[start[0], start[1], 'U']])]

        while queue:
            (x, y), steps, dr, path = queue.pop(0)
            if visited[x][y] or data[x][y] == '#':
                continue
            visited[x][y] = True
            if (x, y) == finish:
                if steps == best_cost:
                    print('another found')
                    pathes.append(path)
                break
            for k, v in directions.items():
                if k == dr:
                    queue.append(((x + v[0], y + v[1]), steps + 1, k, path + [[x + v[0], y + v[1], k]]))
                elif k != opposite[dr]:
                    queue.append(((x + v[0], y + v[1]), steps + 1001, k, path + [[x + v[0], y + v[1], k]]))
            queue = sorted(queue, key=lambda x: x[1])

        data[xx][yy] = '.'
        corners |= after_corners(data, path)

    squares = set()
    for path in pathes:
        for x, y, _ in path:
            squares.add((x, y))

    return len(squares)


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
