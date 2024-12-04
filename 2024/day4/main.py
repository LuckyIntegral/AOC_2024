import os


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
    for line in lines:
        res.append(line)
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    data = parse_data(lines)
    directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
    shape = len(data), len(data[0])
    word = 'XMAS'
    ans = 0

    for row in range(shape[0]):
        for col in range(shape[1]):
            if data[row][col] == 'X':
                for xx, yy in directions:
                    x, y = row, col
                    for char in word[1:]:
                        x += xx
                        y += yy
                        if x < 0 or x >= shape[0] or y < 0 or y >= shape[1] or data[x][y] != char:
                            break
                    else:
                        ans += 1
    return ans


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    shape = len(data), len(data[0])
    ans = 0

    for row in range(shape[0]):
        for col in range(shape[1]):
            if data[row][col] == 'A':
                scr = []
                for xx, yy in directions:
                    x, y = row + xx, col + yy
                    if x in range(shape[0]) and y in range(shape[1]) and data[x][y] in 'MS':
                        scr.append(data[x][y])
                if len(scr) == 4 and scr[0] != scr[1] and scr[2] != scr[3]:
                    ans += 1
    return ans


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
