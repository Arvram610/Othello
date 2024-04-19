import itertools


class Board:
    rows = 8
    cols = 8

    def __init__(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def force_turn(self, x: int, y: int, col: int):
        self.board[y][x] = col

    def turn(self, x: int, y: int, col: int):
        avail_moves = self.gen_avail_moves(col)
        if (x, y) in avail_moves:
            for x, y in avail_moves[(x, y)]:
                self.force_turn(x, y, col)

    def gen_avail_moves(self, col: int) -> dict[tuple[int, int], set[tuple[int, int]]]:
        moves = {}
        for x, y in itertools.product(range(self.cols), range(self.rows)):
            if self.board[y][x] != 0:
                continue
            turns = self.gen_turns(x, y, col)
            if len(turns) < 2:
                continue
            moves[(x, y)] = turns
        return moves

    def gen_turns(self, x: int, y: int, col: int) -> set[tuple[int, int]]:
        turns = set([])
        for dir_x, dir_y in set(itertools.product(range(-1, 2), range(-1, 2))) - {(0, 0)}:
            temp_x, temp_y = x, y
            temp_turns = {(x, y)}
            while True:
                temp_x, temp_y = temp_x + dir_x, temp_y + dir_y
                # If out of bounds
                if not 0 <= temp_x < self.cols or not 0 <= temp_y < self.rows:
                    break
                # If is correct color
                if self.board[temp_y][temp_x] == col:
                    turns = turns.union(temp_turns)
                    break
                # If enemy color
                if self.board[temp_y][temp_x] == -col:
                    temp_turns.add((temp_x, temp_y))
        return turns

    def set_board(self, new_board: list[list[int]]):
        self.board = new_board
        self.rows = len(new_board)
        self.cols = len(new_board[0])

    def debug_print(self):
        for row in self.board:
            for char in row:
                if char == 0:
                    char = 0
                if char == 1:
                    char = 2
                if char == -1:
                    char = 1
                print(char, end="")
            print()


if __name__ == "__main__":
    board = Board()
    board.set_board([[0, 1, -1, 0]])
    board.debug_print()
    board.turn(3, 0, 1)
    board.debug_print()
