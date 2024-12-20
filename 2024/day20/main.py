import argparse
import sys
import os
from functools import cache


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
        res.append(list(line))
    return res


def silver(lines: list[str], limit: int) -> int:
    '''Solves the silver problem'''
    grid = parse_data(lines)
    cost, path = lib.grid_djikstra(grid, lib.grid_find(grid, 'S'), lib.grid_find(grid, 'E'), '.ES')
    cache = {}

    for node, cost_to_end in zip(path, range(cost, -1, -1)):
        cache[node[0]] = cost_to_end, cost - cost_to_end

    ans = 0
    for (x, y), _ in path:
        for dx, dy in lib.DIRS:
            node = (x + dx, y + dy)
            node2 = (x + dx + dx, y + dy + dy)
            if grid[node[0]][node[1]] == '#' and lib.grid_in(grid, *node2)\
                and grid[node2[0]][node2[1]] != '#':
                    new_cost = cache[(x, y)][1] + cache[node2][0] + 2
                    if cost - new_cost >= limit:
                        ans += 1
    return ans


def gold(lines: list[str], limit: int) -> int:
    '''Solves the gold problem'''
    @cache
    def dfs(node: tuple[int, int], deep: int) -> set[tuple[int,int]]:
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
    cost, path = lib.grid_djikstra(grid, lib.grid_find(grid, 'S'), lib.grid_find(grid, 'E'), '.ES')
    dj_cache = {}

    for node, cost_to_end in zip(path, range(cost, -1, -1)):
        dj_cache[node[0]] = cost_to_end, cost - cost_to_end

    ans = 0
    for node, _ in path:
        for nxt in dfs(node, 21):
            mnh = abs(node[0] - nxt[0]) + abs(node[1] - nxt[1])
            new_cost = dj_cache[node][1] + dj_cache[nxt][0] + mnh
            if cost - new_cost >= limit:
                ans += 1
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
    print(f"Silver test: {silver(test, 0)}")
    print(f"Gold test:   {gold(test, 0)}")
    if options.debug:
        return
    print(f"Silver:      {silver(lines, 100)}")
    print(f"Gold:        {gold(lines, 100)}")


if __name__ == "__main__":
    main()
