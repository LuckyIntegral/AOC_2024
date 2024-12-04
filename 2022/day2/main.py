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
        res.append(line.split())
    return res


def silver(lines: list[str]) -> int:
    '''Solves the silver problem'''
    def is_win(a, b) -> int:
        if a == 'A' and b == 'Y': # rock vs paper
            return 2
        if a == 'B' and b == 'Z': # paper vs scissors
            return 2
        if a == 'C' and b == 'X': # scissors vs rock
            return 2
        if a == 'A' and b == 'Z': # rock vs scissors
            return 0
        if a == 'B' and b == 'X': # paper vs rock
            return 0
        if a == 'C' and b == 'Y': # scissors vs paper
            return 0
        return 1
    data = parse_data(lines)
    score = 0
    for game in data:
        score += is_win(game[0], game[1]) * 3
        score += 1 if game[1] == 'X' else 2 if game[1] == 'Y' else 3
    return score


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    def raund(a, b) -> int:
        if b == 'X':
            if a == 'A':
                return 3
            if a == 'B':
                return 1
            if a == 'C':
                return 2
        if b == 'Y':
            if a == 'A':
                return 1
            if a == 'B':
                return 2
            if a == 'C':
                return 3
        if b == 'Z':
            if a == 'A':
                return 2
            if a == 'B':
                return 3
            if a == 'C':
                return 1
    data = parse_data(lines)
    score = 0
    for game in data:
        score += raund(game[0], game[1])
        score += 0 if game[1] == 'X' else 3 if game[1] == 'Y' else 6
    return score


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
