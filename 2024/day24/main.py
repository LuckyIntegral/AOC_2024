import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib
from collections import deque
import re

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
    stack = []

    for line in lines:
        if line == '':
            stack = res
            res = []
        else:
            res.append(line)
    return stack, res


def calculate(wires: deque, values: dict) -> int:

    while wires:
        first, operator, second, res = wires.popleft()

        if first not in values.keys() or second not in values.keys():
            wires.append((first, operator, second, res))
            continue

        if operator == 'AND':
            values[res] = values[first] & values[second]
        elif operator == 'XOR':
            values[res] = values[first] ^ values[second]
        elif operator == 'OR':
            values[res] = values[first] | values[second]

    keys = filter(lambda x: x.startswith('z'), values.keys())
    res = ''.join([str(values[k]) for k in sorted(keys, reverse=True)])
    return int(res, base=2)


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    wires = deque()
    values = {}

    for line in data[0]:
        splitted = line.split(': ')
        values[splitted[0]] = int(splitted[1])

    for line in data[1]:
        wires.append((re.match(r'(\w+) (\w+) (\w+) -> (\w+)', line).groups()))

    return calculate(wires, values)


def analyze(wires, print_key: bool = False) -> any:
    def dfs(key: str, level: int = 0):
        prefix = f'{key}=' if print_key else ''
        values = visual[key]
        if values[0].startswith('x') or values[0].startswith('y'):
            return prefix + f'({values[0]} {values[1]} {values[2]})'
        first = dfs(values[0], level + 1)
        second = dfs(values[2], level + 1)
        if first < second:
            return prefix + f'({first} {values[1]} {second})'
        return prefix + f'({second} {values[1]} {first})'

    visual = {}
    annotations = {
        'AND': '&',
        'OR': '|',
        'XOR': '^'
    }
    for first, operation, second, result in wires:
        operation = annotations[operation]
        visual[result] = [first, operation, second]

    for k in sorted(filter(lambda x: x.startswith('z'), visual.keys())):
        print(k,"=",dfs(k))


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    values = {}
    wires = deque()
    to_swap = {
        'qgd': 'z18',
        'z18': 'qgd',
        'mwk': 'z10',
        'z10': 'mwk',
        'jmh': 'hsw',
        'hsw': 'jmh',
        'gqp': 'z33',
        'z33': 'gqp',
    }

    N = len(data[0]) // 2
    X = 21475712124771
    Y = 33740322330241

    for i in range(N):
        values[f'x{i:02}'] = (X >> i) & 1
        values[f'y{i:02}'] = (Y >> i) & 1

    for line in data[1]:
        first, operator, second, result = (re.match(r'(\w+) (\w+) (\w+) -> (\w+)', line).groups())
        if result in to_swap.keys():
            result = to_swap[result]
        wires.append((first, operator, second, result))

    res = calculate(wires, values)
    exp = X + Y
    print(f'{X} + {Y} = {exp} / {res}')

    print(''.join([str(values[f'x{v:02}']) for v in range(N)]))
    print('+')
    print(''.join([str(values[f'y{v:02}']) for v in range(N)]))
    print('=')
    print(''.join([str(res >> v & 1) for v in range(N+1)]))
    print('exp')
    print(''.join([str(exp >> v & 1) for v in range(N+1)]))

    return ','.join(sorted(to_swap.keys()))


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
