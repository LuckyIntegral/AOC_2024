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
            commands += [list(map(int, option[1:-1].split(',')))]

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
        cmds = []
        for option in commands:
            cmd = sum(1 << bit for bit in option)
            cmds.append(cmd)
        round = bfs(state, cmds)
        res += round

    return res


from z3 import Int, Optimize, sat
def gold(content: str):
    '''Solves the gold problem'''
    def list_sum(N: int, *args: list[int]) -> list[int]:
        res = [0] * N
        for lst in args:
            for i in range(N):
                res[i] += lst[i]
        return res

    def list_add(nbr: int, a: list[int]) -> list[int]:
        return [nbr * x for x in a]

    data = parse_data(content)
    res = 0

    for line in data:
        _, commands, limits = line
        masked = []
        for command in commands:
            mask = [0] * len(limits)
            for bit in command:
                mask[bit] = 1
            masked.append(mask)

        vs = []
        for i, command in enumerate(masked):
            vs.append((Int(f'{chr(ord("A") + i)}'), command))

        solver = Optimize()
        summed = list_sum(len(limits), *[list_add(a,b) for a, b in vs])

        solver.add([a >= 0 for a, _ in vs])
        solver.add([summed[i] == limits[i] for i in range(len(limits))])

        solver.minimize(sum(a for a, _ in vs))

        assert solver.check() == sat

        model = solver.model()
        res += sum(model.eval(var).as_long() for var, _ in vs)

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
