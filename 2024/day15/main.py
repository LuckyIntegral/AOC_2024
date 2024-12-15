import argparse
import sys
import os
from functools import wraps

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
    moves = []
    for line in lines:
        if line:
            moves.append(line)
        else:
            res.append(moves)
            moves = []
    return res, moves


def grid_rotation_wrapper(func):
    @wraps(func)
    def wrapper(maze: list[str], dirr: str, *args, **kwargs):
        match dirr:
            case '^':
                maze = lib.grid_rotate(maze)
                maze = lib.grid_rotate(maze)
                maze = lib.grid_rotate(maze)
            case 'v':
                maze = lib.grid_rotate(maze)
            case '>':
                maze = lib.grid_rotate(maze)
                maze = lib.grid_rotate(maze)

        result = func(maze, dirr, *args, **kwargs)

        match dirr:
            case '^':
                result = lib.grid_rotate(result)
            case 'v':
                result = lib.grid_rotate(result)
                result = lib.grid_rotate(result)
                result = lib.grid_rotate(result)
            case '>':
                result = lib.grid_rotate(result)
                result = lib.grid_rotate(result)
        return result
    return wrapper


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    @grid_rotation_wrapper
    def move_box(maze: list[str], _: str) -> None:
        r, c = lib.grid_find(maze, '@')
        ll = 1
        while maze[r][c - ll] == 'O':
            ll += 1
        if maze[r][c - ll] == '.':
            maze[r][c - ll] = 'O'
            maze[r][c - 1] = '@'
            maze[r][c] = '.'
        return maze

    maze, moves = parse_data(lines)
    maze = [list(line) for line in maze[0]]
    moves = ''.join(moves)

    for char in moves:
        r, c = lib.grid_find(maze, '@')
        rr, cc = lib.DIRS_ARROWS[char]
        if maze[rr+r][cc+c] == '.':
            maze[r+rr][c+cc] = '@'
            maze[r][c] = '.'
        elif maze[rr+r][cc+c] == 'O':
            maze = move_box(maze, char)

    return sum(row * 100 + col for row, line in enumerate(maze) for col, char in enumerate(line) if char == 'O')


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    @grid_rotation_wrapper
    def move_box(maze: list[str], dirr: str) -> None:
        def pair(maze: list[str], point: tuple[int, int, str]) -> set[tuple[int,int,str]]:
            r, c = point[0], point[1]
            rr, cc = lib.DIRS_ARROWS[dirr]
            points = set([(r, c, maze[r][c])])

            if dirr in '^v':
                if maze[r][c] == ']':
                    points.add((r - rr, c - cc, maze[r - rr][c - cc]))
                else:
                    points.add((r + rr, c + cc, maze[r + rr][c + cc]))
            else:
                if maze[r][c] == '[':
                    points.add((r - rr, c - cc, maze[r - rr][c - cc]))
                else:
                    points.add((r + rr, c + cc, maze[r + rr][c + cc]))
            return points

        robot = lib.grid_find(maze, '@')
        seen = set()
        boxes = pair(maze, (robot[0], robot[1] - 1))

        while boxes:
            poped = boxes.pop()
            if poped in seen:
                continue
            seen.add(poped)
            r, c, _ = poped
            if maze[r][c - 1] == '#':
                return maze
            if maze[r][c - 1] != '.':
                boxes |= pair(maze, (r, c - 1))

        for r, c, _ in seen:
            maze[r][c] = '.'
        for r, c, char in seen:
            maze[r][c-1] = char
        maze[robot[0]][robot[1] - 1] = '@'
        maze[robot[0]][robot[1]] = '.'
        return maze

    temp, moves = parse_data(lines)
    char_map = {
        '@': '@.',
        '#': '##',
        'O': '[]',
        '.': '..'
    }
    maze = []

    for line in temp[0]:
        maze.append(list(''.join(char_map[char] for char in line)))
    moves = ''.join(moves)

    for char in moves:
        r, c = lib.grid_find(maze, '@')
        rr, cc = lib.DIRS_ARROWS[char]

        if maze[r+rr][c+cc] == '.':
            maze[r][c] = '.'
            maze[r+rr][c+cc] = '@'
        elif maze[rr + r][cc + c] in '[]':
            maze = move_box(maze, char)

    return sum(row * 100 + col for row, line in enumerate(maze) for col, char in enumerate(line) if char == '[')


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
