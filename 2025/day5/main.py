import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    return [content.splitlines() for content in content.strip().split('\n\n')]


def silver(content: str):
    '''Solves the silver problem'''
    conditions, lines = parse_data(content)
    res = 0

    for line in lines:
        nbr = int(line)
        for condition in conditions:
            start, end = map(int, condition.split('-'))
            if start <= nbr <= end:
                res += 1
                break

    return res


def gold(content: str):
    '''Solves the gold problem'''
    conditions, _ = parse_data(content)
    intervals = []

    for cond in conditions:
        start, end = map(int, cond.split('-'))
        intervals.append((start, end))

    intervals.sort()
    merged = []
    current_start, current_end = intervals[0]

    for start, end in intervals[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    merged.append((current_start, current_end))

    total = 0
    for start, end in merged:
        total += end - start + 1

    return total


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
