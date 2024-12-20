import argparse
import sys
import os
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


import heapq

def grid_djikstra(
    grid: list[str],
    start: tuple[int, int],
    end: tuple[int, int],
    surface: list[str],
    calculate_cost: callable = lambda grid, cost, path: cost+1
) -> int:
    '''Applies Djikstra algorithm for the grid'''
    size = lib.grid_size(grid)
    visited = [[False] * size[1] for _ in range(size[0])]
    heap = [(0, [(start, 'Init point')])]

    while heap:
        steps, path = heapq.heappop(heap)
        (row, col), _ = path[-1]
        if visited[row][col] or grid[row][col] not in surface:
            continue
        visited[row][col] = True
        if (row, col) == end:
            return steps, path
        for key, (drow, dcol) in lib.DIRS_CHARS.items():
            nxt = path+[((row+drow, col+dcol), key)]
            heapq.heappush(heap, (calculate_cost(grid, steps, nxt), nxt))

    return -1, []


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
    grid = parse_data(lines)
    cost, path = grid_djikstra(grid, lib.grid_find(grid, 'S'), lib.grid_find(grid, 'E'), '.ES')
    cache = {}

    for node, cost_to_end in zip(path, range(cost, -1, -1)):
        cache[node[0]] = cost_to_end, cost - cost_to_end

    saved = defaultdict(int)
    for (x, y), _ in path:
        for dx, dy in lib.DIRS:
            node = (x + dx, y + dy)
            node2 = (x + dx + dx, y + dy + dy)
            if grid[node[0]][node[1]] == '#' and lib.grid_in(grid, *node2):
                if node2 in cache.keys():
                    new_cost = cache[(x, y)][1] + cache[node2][0] + 2
                    if cost - new_cost >= 100:
                        saved[cost - new_cost] += 1

    return sum(v for v in saved.values())

from functools import cache
def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    @cache
    def dfs(node: tuple[int, int], deep: int) -> set[tuple[int,int]]:
        '''from - to - min in range steps cached bfs'''
        if not lib.grid_in(grid, *node) or deep == 0:
            return set()

        seen = set()
        if grid[node[0]][node[1]] != '#':
            seen.add(node)

        for dx, dy in lib.DIRS:
            nxt = node[0] + dx, node[1] + dy
            seen |= dfs(nxt, deep - 1)
        return seen

    grid = parse_data(lines)
    cost, path = grid_djikstra(grid, lib.grid_find(grid, 'S'), lib.grid_find(grid, 'E'), '.ES')
    dj_cache = {}

    for node, cost_to_end in zip(path, range(cost, -1, -1)):
        dj_cache[node[0]] = cost_to_end, cost - cost_to_end

    saved = defaultdict(int)
    for node, _ in path:
        to_check = dfs(node, 21) # i hope it will be cached

        for nxt in to_check:
            mnh = abs(node[0] - nxt[0]) + abs(node[1] - nxt[1])

            assert nxt in dj_cache and mnh <= 20

            new_cost = dj_cache[node][1] + dj_cache[nxt][0] + mnh

            if cost - new_cost >= 100:
                saved[cost - new_cost] += 1

    return sum(v for v in saved.values())


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
