import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


from collections import defaultdict
def parse_data(content: str):
    '''Parses the data'''
    lines = content.splitlines()
    graph = defaultdict(list)

    for line in lines:
        graph[line[:3]] = line[5:].split(' ')

    return graph


def silver(content: str):
    '''Solves the silver problem'''
    def dfs(node: str) -> int:
        if node == 'out':
            return 1
        paths = 0
        for nxt in data[node]:
            paths += dfs(nxt)
        return paths

    data = parse_data(content)
    res = 0

    for nbr in data['you']:
        res += dfs(nbr)

    return res


from functools import cache
def gold(content: str):
    '''Solves the gold problem'''
    @cache
    def dfs(node: str, dac: bool = False, fft: bool = False) -> int:
        if node == 'out':
            return 1 if dac and fft else 0
        if node == 'dac':
            dac = True
        if node == 'fft':
            fft = True
        paths = 0
        for nxt in data[node]:
            paths += dfs(nxt, dac, fft)
        return paths

    data = parse_data(content)
    res = 0

    for nbr in data['svr']:
        res += dfs(nbr)

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
