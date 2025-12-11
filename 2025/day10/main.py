import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    lines = [line.split(' ') for line in content.splitlines()]
    res = []
    for line in lines:
        lights = 0
        for i, bit in enumerate(line[0][1:-1]):
            lights |= 1 << i if bit == '#' else 0

        commands = []
        for option in line[1:-1]:
            cmd = 0
            for bit in map(int, option[1:-1].split(',')):
                cmd |= 1 << bit
            commands += [cmd]

        limits = list(map(int, line[-1][1:-1].split(',')))
        res += [(lights, commands, limits)]
    return res


import heapq
def silver(content: str):
    '''Solves the silver problem'''
    def bfs(state: int, commands: list[int]):
        heap = [(0, 0)]
        seen = set()

        while heap:
            rounds, curr = heapq.heappop(heap)
            if curr == state:
                return rounds
            if curr in seen:
                continue
            seen.add(curr)

            for cmd in commands:
                heapq.heappush(heap, (rounds + 1, curr ^ cmd))

    data = parse_data(content)
    res = 0

    for line in data:
        state, commands, _ = line
        round = bfs(state, commands)
        res += round

    return res


def gold(content: str):
    '''Solves the gold problem'''
    # def bfs(commands: list[int], limits: list[int]):
    #     heap = [(0, tuple([0] * len(limits)))]
    #     seen = set()

    #     while heap:
    #         rounds, lims = heapq.heappop(heap)

    #         if lims in seen:
    #             continue
    #         seen.add(lims)

    #         if lims == tuple(limits):
    #             return rounds

    #         for cmd in commands:
    #             new_lims = list(lims)
    #             valid = True
    #             for i in range(len(limits)):
    #                 if (cmd >> i) & 1:
    #                     new_lims[i] += 1
    #                     if new_lims[i] > limits[i]:
    #                         valid = False
    #                         break
    #             if valid:
    #                 heapq.heappush(heap, (rounds + 1, tuple(new_lims)))

    # data = parse_data(content)
    # res = 0

    # for line in data:
    #     _, commands, limits = line
    #     round = bfs(commands, limits)
    #     print(round)
    #     res += round

    return 0


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
