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
    epsilon = [0] * len(data[0])
    gamma = [0] * len(data[0])
    for line in data:
        for idx, char in enumerate(line):
            epsilon[idx] += 1 if char == '1' else 0
    for idx, char in enumerate(epsilon):
        epsilon[idx] = '0' if char > len(data) // 2 else '1'
        gamma[idx] = '1' if epsilon[idx] == '0' else '0'
    return int(''.join(epsilon), 2) * int(''.join(gamma), 2)


def gold(lines: list[str]) -> int:
    '''Solves the gold problem'''
    data = parse_data(lines)
    epsilon = data
    gamma = data

    i = 0
    while len(epsilon) > 1 and i < len(data[0]):
        o, z = 0, 0
        for line in epsilon:
            if line[i] == '1':
                o += 1
            else:
                z += 1
        if o >= z:
            epsilon = [line for line in epsilon if line[i] == '1']
        else:
            epsilon = [line for line in epsilon if line[i] == '0']
        i += 1

    i = 0
    while len(gamma) > 1 and i < len(data[0]):
        o, z = 0, 0
        for line in gamma:
            if line[i] == '1':
                o += 1
            else:
                z += 1
        if o >= z:
            gamma = [line for line in gamma if line[i] == '0']
        else:
            gamma = [line for line in gamma if line[i] == '1']
        i += 1

    return int(epsilon[0], 2) * int(gamma[0], 2)


def main():
    '''Parses the input and solves the two problems'''
    lines, test = content()
    print(f"Silver test: {silver(test)}")
    print(f"Gold test:   {gold(test)}")
    print(f"Silver:      {silver(lines)}")
    print(f"Gold:        {gold(lines)}")


if __name__ == "__main__":
    main()
