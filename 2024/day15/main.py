import argparse
import sys
import os

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


def find_robot(maze: list[str], to_find: str) -> tuple[int, int]:
    '''Finds the robot in the maze'''
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if char == to_find:
                return row, col
    return -1, -1


def rotate_box_right(maze: list[list[str]]) -> list[list[str]]:
    '''Rotates the box in the maze by 90 degrees'''
    new = [[] for _ in range(len(maze[0]))]

    for line in maze[::-1]:
        for col, char in enumerate(line):
            new[col].append(char)
    return new


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    def move_box(maze: list[str], dirr: str) -> None:
        match dirr:
            case '^':
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
            case 'v':
                maze = rotate_box_right(maze)
            case '>':
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
            case '<':
                pass

        r, c = find_robot(maze, '@')
        ll = 1

        while maze[r][c - ll] == 'O':
            ll += 1
        if maze[r][c - ll] == '.':
            maze[r][c - ll] = 'O'
            maze[r][c - 1] = '@'
            maze[r][c] = '.'

        match dirr:
            case '^':
                maze = rotate_box_right(maze)
            case 'v':
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
            case '>':
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
            case '<':
                pass
        return maze
    maze, moves = parse_data(lines)
    maze = [list(line) for line in maze for line in line]
    moves = ''.join(moves)
    dirs = {
        '<': (0, -1),
        '>': (0, 1),
        '^': (-1, 0),
        'v': (1, 0)
    }

    for char in moves:
        r, c = find_robot(maze, '@')
        rr, cc = dirs[char]
        if maze[rr + r][cc + c] == '.':
            maze[r][c] = '.'
            r += rr
            c += cc
            maze[r][c] = '@'
        elif maze[rr + r][cc + c] == 'O':
            maze = move_box(maze, char)
        elif maze[rr + r][cc + c] == '#':
            r += rr
            c += cc
        else:
            print(f"Error: {maze[rr + r][cc + c]}")

    ans = 0
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if char == 'O':
                ans += row * 100 + col
    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def move_box(maze: list[str], dirr: str) -> None:
        def pair(maze: list[str], point: tuple[int, int, str]) -> tuple[int,int]:
            '''Returns point related to the matched box'''
            r, c = point[0], point[1]
            match dirr:
                case '^':
                    if maze[r][c] == '[':
                        return(r - 1, c, ']')
                    else:
                        return(r + 1, c, '[')
                case 'v':
                    if maze[r][c] == '[':
                        return(r + 1, c, ']')
                    else:
                        return(r - 1, c, '[')
                case '>':
                    if maze[r][c] == '[':
                        return(r, c - 1, ']')
                    else:
                        return(r, c + 1, '[')
                case '<':
                    if maze[r][c] == '[':
                        return(r, c + 1, ']')
                    else:
                        return(r, c - 1, '[')
            return None # should never happen
        match dirr:
            case '^':
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
            case 'v':
                maze = rotate_box_right(maze)
            case '>':
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
            case '<':
                pass

        rrr, ccc = find_robot(maze, '@')
        boxes = set()
        boxes.add((rrr, ccc - 1, maze[rrr][ccc-1]))
        boxes.add(pair(maze, (rrr, ccc - 1)))
        move = True

        while move:
            before = len(boxes)
            neighbors = set()
            for box in boxes:
                r, c, _ = box
                match maze[r][c - 1]:
                    case '[' | ']':
                        neighbors.add((r, c - 1, maze[r][c - 1]))
                        neighbors.add(pair(maze, (r, c - 1)))
                    case '#':
                        move = False
                    case '.':
                        r += 0 # idk why pass is not working
            boxes = boxes | neighbors
            if before == len(boxes):
                break

        if move:
            for r, c, _ in boxes:
                maze[r][c] = '.'
            for r, c, char in boxes:
                maze[r][c-1] = char
            maze[rrr][ccc] = '.'
            maze[rrr][ccc-1] = '@'


        match dirr:
            case '^':
                maze = rotate_box_right(maze)
            case 'v':
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
            case '>':
                maze = rotate_box_right(maze)
                maze = rotate_box_right(maze)
            case '<':
                pass
        return maze
    temp, moves = parse_data(lines)
    maze = []
    for line in temp[0]:
        buffer = ''
        for char in line:
            match char:
                case '@':
                    buffer += '@.'
                case '#':
                    buffer += '##'
                case 'O':
                    buffer += '[]'
                case '.':
                    buffer += '..'
        maze.append(list(buffer))
    moves = ''.join(moves)
    dirs = {
        '<': (0, -1),
        '>': (0, 1),
        '^': (-1, 0),
        'v': (1, 0)
    }

    for char in moves:
        r, c = find_robot(maze, '@')
        rr, cc = dirs[char]

        if maze[rr + r][cc + c] == '.':
            maze[r][c] = '.'
            r += rr
            c += cc
            maze[r][c] = '@'
        elif maze[rr + r][cc + c] in '[]':
            maze = move_box(maze, char)
        elif maze[rr + r][cc + c] == '#':
            r += rr
            c += cc
        else:
            print(f"Error: {maze[rr + r][cc + c]}")

    print(f'dir {char}')
    for line in maze:
        print(''.join(line))
    print()

    ans = 0
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if char == '[':
                ans += row * 100 + col
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
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    if options.debug:
        return
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
