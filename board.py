import itertools


class Board:
    rows = 8
    cols = 8

    def __init__(self):
        self.avail_moves = None
        self.last_avail_moves = None
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.player = 1
        self.gen_avail_moves(self.player)

    def force_turn(self, x: int, y: int, col: int):
        self.board[y][x] = col

    def turn(self, x: int, y: int):
        if self.avail_moves == self.last_avail_moves:
            return
        if (x, y) in self.avail_moves:
            for x, y in self.avail_moves[(x, y)]:
                self.force_turn(x, y, self.player)
        self.player = -self.player

    def check_move_available(self):
        self.gen_avail_moves(self.player)
        if len(self.avail_moves) == 0:
            return False
        return True

    def switch_player(self):
        self.player = -self.player
    def gen_avail_moves(self, col: int) -> dict[tuple[int, int], set[tuple[int, int]]]:
        moves = {}
        for x, y in itertools.product(range(self.cols), range(self.rows)):
            if self.board[y][x] != 0:
                continue
            if (x,y) == (3,0):
                pass
            turns = self.gen_turns(x, y, col)
            if len(turns) < 2:
                continue
            moves[(x, y)] = turns

        self.last_avail_moves, self.avail_moves = self.avail_moves, moves
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

    def debug_set_board(self, new_board: list[list[int]]):
        self.board = new_board
        self.rows = len(new_board)
        self.cols = len(new_board[0])
        self.gen_avail_moves(self.player)

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
    board.debug_set_board([[0, 1, -1, 0]])
    assert board.board == [[0, 1, -1, 0]]
    board.turn(3, 0)
    assert board.board == [[0, 1, 1, 1]]
