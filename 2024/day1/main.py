from collections import defaultdict as dd
import os


def content() -> list[str]:
    '''Reads the input file and returns a list of strings'''
    with open('input.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    if not os.path.exists('test.txt'):
        return lines, []

    with open('test.txt') as f:
        test = f.readlines()
    test = [line.strip() for line in test]

    return lines, test


def parse_data(lines: list[str]) -> tuple[list[int], list[int]]:
    '''Parses the data'''
    l, r = [], []

    for line in lines:
        n = line.strip().split('  ')
        l.append(int(n[0]))
        r.append(int(n[1]))

    return l, r


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    l, r = parse_data(lines)

    l.sort()
    r.sort()

    return sum(abs(a - b) for a, b in zip(l, r))


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    counter = dd(int)
    l = []

    for line in lines:
        n = line.strip().split('  ')
        l.append(int(n[0]))
        counter[int(n[1])] += 1

    return sum(n * counter[n] for n in l)


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    if test:
        print(f"Silver test: {silver(test)}")
        print(f"Gold test:   {gold(test)}")
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
