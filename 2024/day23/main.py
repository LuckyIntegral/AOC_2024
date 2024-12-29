import argparse
import sys
import os
from collections import defaultdict

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
    res = defaultdict(set)
    for line in lines:
        a, b = line.split('-')
        res[a].add(b)
        res[b].add(a)
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    graph = parse_data(lines)
    triples = set()

    for edge in graph:
        for edge2 in graph[edge]:
            for shared in graph[edge] & graph[edge2]:
                triples.add(tuple(sorted([edge, edge2, shared])))

    return sum(1 for triple in triples if any(edge.startswith('t') for edge in triple))


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def bron_kerbosch(candidates, constructed):
        if not candidates:
            networks.append(constructed)
            return
        for v in candidates.copy():
            bron_kerbosch(candidates & graph[v], constructed | set([v]))
            candidates.remove(v)

    graph = parse_data(lines)
    candidates = set(graph.keys())
    constructed = set()
    networks = []
    bron_kerbosch(candidates, constructed)
    return ','.join(sorted((max(networks, key=len))))


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
