import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from lib import lib

INPUT_FILE = os.path.join(os.path.dirname(__file__), 'input.txt')
TEST_FILE = os.path.join(os.path.dirname(__file__), 'test.txt')


def parse_data(content: str):
    '''Parses the data'''
    data = content.split('\n\n')
    shapes = []
    for shape in data[:-1]:
        shapes.append(shape.splitlines()[1:])

    regions = []
    for line in data[-1].splitlines():
        sizes, qs = line.split(': ')
        rows, cols = map(int, sizes.split('x'))
        qs = list(map(int, qs.split(' ')))
        regions.append((cols, rows, qs))
    return shapes, regions

import time
def silver(content: str):
    '''Solves the silver problem'''
    timeout_flag = [False]
    start_time = [None]
    def backtrack(grid, qs, step, rows, cols, start_pos = 0) -> bool:
        if time.time() - start_time[0] > 0.1:
            timeout_flag[0] = True
            return False

        if step == len(qs):
            return True
        if qs[step] == 0:
            return backtrack(grid, qs, step + 1, rows, cols)

        for pos in range(start_pos, rows * cols):
            row = pos // cols
            col = pos % cols

            if row > rows - 3 or col > cols - 3:
                continue

            for shape in shape_masks[step]:
                if (grid[row] & (shape[0] << col)) | \
                    (grid[row + 1] & (shape[1] << col)) | \
                    (grid[row + 2] & (shape[2] << col)):
                    continue
                grid[row] |= shape[0] << col
                grid[row + 1] |= shape[1] << col
                grid[row + 2] |= shape[2] << col
                qs[step] -= 1

                next_step = step if qs[step] > 0 else step + 1
                if backtrack(grid, qs, next_step, rows, cols, pos + 1):
                    return True

                grid[row] ^= shape[0] << col
                grid[row + 1] ^= shape[1] << col
                grid[row + 2] ^= shape[2] << col
                qs[step] += 1

        return False

    shapes, regions = parse_data(content)
    shape_masks = []

    for shape in shapes:
        mutation_masks = set()
        for _ in range(4):
            shape = lib.grid_rotate(shape)
            mutation_masks.add(tuple(sum(1 << idx if char == '#' else 0 for idx, char in enumerate(line)) for line in shape[::-1]))
            mutation_masks.add(tuple(sum(1 << idx if char == '#' else 0 for idx, char in enumerate(line)) for line in shape))
        shape_masks.append(mutation_masks)

    res = 0
    for i, (rows, cols, qs) in enumerate(regions):
        grid = [0] * rows
        timeout_flag[0] = False
        start_time[0] = time.time()

        if backtrack(grid, qs, 0, rows, cols):
            res += 1
            print(f"{i}/{len(regions)} Region {rows}x{cols} is +1 and results in {res} with time {time.time() - start_time[0]:.2f}s")
        elif timeout_flag[0]:
            print(f"{i}/{len(regions)} Region {rows}x{cols} with quantities {qs} timed out - skipping")

    return res


def gold(content: str):
    '''Solves the gold problem'''
    data = parse_data(content)
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
