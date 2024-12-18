import argparse
import sys
import os
import heapq
from collections import deque

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
        res.append(list(map(int, line.split(','))))
    return res


def silver(lines: list[str], size) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    maze = [['.' for _ in range(size[0] + 1)] for _ in range(size[1] + 1)]
    for x, y in data[:size[2]]:
        maze[x][y] = '#'
    start = (0, 0)
    end = (size[0], size[1])

    visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    heap = [(0, start, 'R'), (0, start, 'D')]
    heapq.heapify(heap)
    directions = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }

    while heap:
        steps, (x, y), dr = heapq.heappop(heap)
        if not lib.grid_in(maze, x, y):
            continue
        if visited[x][y] or maze[x][y] == '#':
            continue
        visited[x][y] = True
        if (x, y) == end:
            return steps
        for k, v in directions.items():
            if k == dr:
                heapq.heappush(heap, (steps + 1, (x + v[0], y + v[1]), k))
            else:
                heapq.heappush(heap, (steps + 1, (x + v[0], y + v[1]), k))

    return -1


def gold(lines: list[str], size) -> int:
    '''Solves the gold problem'''
    def dfs(maze, start, end):
        visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
        dq = deque([(start)])

        while dq:
            x, y = dq.popleft()
            if not lib.grid_in(maze, x, y):
                continue
            if visited[x][y] or maze[x][y] == '#':
                continue
            visited[x][y] = True
            if visited[end[0]][end[1]]:
                return True
            for xx, yy in lib.DIRS:
                dq.appendleft((x + xx, y + yy))

        return False

    data = parse_data(lines)
    maze = [['.' for _ in range(size[0] + 1)] for _ in range(size[1] + 1)]

    for x, y in data[:size[2]]:
        maze[x][y] = '#'
    start = (0, 0)
    end = (size[0], size[1])

    ans = size[2]
    for x, y in data[size[2]:]:
        maze[x][y] = '#'
        if not dfs(maze, start, end):
            break
        ans += 1

    return f'{data[ans][0]},{data[ans][1]}'


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
    size = (6, 6, 12)
    print(f"Silver test: {silver(test, size)}")
    print(f"Gold test:   {gold(test, size)}")
    if options.debug:
        return
    size = (70, 70, 1024)
    print(f"Silver:      {silver(lines, size)}")
    print(f"Gold:        {gold(lines, size)}")


if __name__ == "__main__":
    main()
