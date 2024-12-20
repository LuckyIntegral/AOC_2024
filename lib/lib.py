import heapq

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIRS_8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
DIRS_PATTERN_SEARCH = [(0, 1), (1, 1), (1, 0), (1, -1)]

DIRS_ARROWS = {'<':(0, -1), '>':(0, 1), '^':(-1, 0), 'v':(1, 0)}
DIRS_OPPOSITE_ARROWS = {'<': '>', '>': '<', 'v': '^', '^': 'v'}

DIRS_CHARS = {'U':(-1, 0), 'D':(1, 0), 'L':(0, -1), 'R':(0, 1)}
DIRS_OPPOSITE_CHARS = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}


# at this point i started thinking about a Grid class
def grid_size(data: list[str]) -> tuple[int, int]:
    '''Returns the size of the grid (shape)'''
    return len(data), len(data[0])


def grid_in(data: list[str], row: int, col: int) -> bool:
    '''Checks if a point is in the grid'''
    return 0 <= row < len(data) and 0 <= col < len(data[0])


def grid_djikstra(
    grid: list[str],
    start: tuple[int, int],
    end: tuple[int, int],
    surface: list[str],
    calculate_cost: callable = lambda grid, cost, path: cost+1
) -> int:
    '''Applies Djikstra algorithm for the grid'''
    size = grid_size(grid)
    visited = [[False] * size[1] for _ in range(size[0])]
    heap = [(0, [(start, 'Init point')])]

    while heap:
        steps, path = heapq.heappop(heap)
        (row, col), _ = path[-1]
        if visited[row][col] or grid[row][col] not in surface:
            continue
        visited[row][col] = True
        if (row, col) == end:
            return steps, path
        for key, (drow, dcol) in DIRS_CHARS.items():
            nxt = path+[((row+drow, col+dcol), key)]
            heapq.heappush(heap, (calculate_cost(grid, steps, nxt), nxt))

    return -1, []


def grid_find(maze: list[str], to_find: str, find_all: bool = False) -> list[tuple[int, int]] | tuple[int, int]:
    '''Finds the first or all instances of a character in a grid

    Args:
        maze (list[str]): the grid to search
        to_find (str): the character to find
        find_all (bool): whether to return all instances or the first

    Returns:
        list[tuple[int, int]] | tuple[int, int]: the points of the character
    '''
    res = []
    for row, line in enumerate(maze):
        for col, char in enumerate(line):
            if char == to_find:
                if not find_all:
                    return row, col
                res.append((row, col))
    return res


def grid_rotate(data: list[str] | list[list[str]]) -> list[list[str]]:
    '''Rotates the grid 90 degrees clockwise

    Args:
        data (list[str]): the grid to rotate

    Returns:
        list[str]: the rotated grid by 90 degrees clockwise
    '''
    rotated = [[] for _ in range(len(data[0]))]

    for line in data[::-1]:
        for col, char in enumerate(line):
            rotated[col].append(char)
    return rotated


def grid_dfs(
    data: list[str],
    pattern: str,
    direction = DIRS,
    hashing = False,
    straight = False,
) -> list[list[int]]:
    '''Finds the pattern in the grid

    Args:
        data (list[str]): the grid
        pattern (str): the sequence to find
        hashing (bool): whether to store the seen points
        straight (bool): whether the pattern has to be in a straight line
        dirs (list[tuple[int]]): the directions to move

    Returns:
        list[list[int]]: the final points
    '''
    def dfs(row: int,
        col: int,
        iter: int,
        hash: list[list[bool]],
        dirs: list[tuple[int,int]]
    ) -> list[list]:
        if not (0 <= row < len(data) and 0 <= col < len(data[0])\
            and data[row][col] == pattern[iter] and iter < len(pattern)):
            return []

        if hashing and hash[row][col]: return []
        if hashing: hash[row][col] = True

        if iter == len(pattern) - 1:
            if data[row][col] == pattern[iter]:
                return [[row, col]]
            return []

        res = []
        for rr, cc in direction:
            res += dfs(row + rr, col + cc, iter + 1, hash, dirs)
        return res

    res = []
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == pattern[0]:
                seen = [[False] * len(data[0]) for _ in range(len(data))]
                if straight:
                    for direct in direction:
                        res += dfs(row + direct[0], col + direct[1], 1, seen, direct)
                else:
                    res += dfs(row, col, 0, seen, direction)
    return res
