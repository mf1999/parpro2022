ILLEGAL_MOVE = 100
NO_WINNER = 101
WINNER = 102

import copy

class Board:

    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.board = []
        self.col_full = [False, False, False, False, False, False, False]
        self.init_board()

    def init_board(self):
        for i in range(self.n):
            self.board.append([])
            for j in range(self.m):
                self.board[i].append(0)

    def show(self):
        print(f"=\t" * (self.m + 2), flush=True)
        for i in range(self.n):
            self.col_full.append(False)
            print('|\t', end='', flush=True)
            for j in range(self.m):
                print(f"{self.board[i][j]}\t", end='', flush=True)
            print('|')
        print(f"=\t" * (self.m + 2), flush=True)

    def is_legal(self, col: int):
        if col < 0 or col >= self.m:
            return False
        #print(f"{self.col_full}")
        if self.col_full[col]:
            return False
        return True

    def __drop_marker(self, col: int, marker: int):
        for i in range(self.n - 1, -1, -1):
            if self.board[i][col] == 0:
                self.board[i][col] = marker
                return True
        return False

    def __check_column_full(self, col: int):
        if self.board[0][col] != 0:
            return True
        return False

    def __check_vertical(self, col: int, marker: int):
        ctr = 0
        for i in range(self.n - 1, -1, -1):
            if self.board[i][col] != marker:
                ctr = 0
            else:
                ctr += 1
            if ctr == 4:
                return True
        return False

    def __check_horizontal(self, col: int, marker: int):
        i = 0
        for i in range(self.n - 1, -1, -1):
            if self.board[i][col] == 0:
                i += 1
                break

        ctr = 0
        for j in range(0, self.m):
            if self.board[i][j] != marker:
                ctr = 0
            else:
                ctr += 1
            if ctr == 4:
                return True
        return False

    def __check_left_diagonal(self, col: int, marker: int):
        i = 0
        for i in range(self.n - 1, -1, -1):
            if self.board[i][col] == 0:
                i += 1
                break

        j = col
        while i != 0 and j != 0:
            i -= 1
            j -= 1

        ctr = 0
        while i < self.n and j < self.m:
            if self.board[i][j] != marker:
                ctr = 0
            else:
                ctr += 1
            if ctr == 4:
                return True
            i += 1
            j += 1
        return False

    def __check_right_diagonal(self, col: int, marker: int):
        i = 0
        for i in range(self.n - 1, -1, -1):
            if self.board[i][col] == 0:
                i += 1
                break

        j = col
        while i < self.n - 1 and j != 0:
            i += 1
            j -= 1

        ctr = 0
        while i > -1 and j < self.m:
            if self.board[i][j] != marker:
                ctr = 0
            else:
                ctr += 1
            if ctr == 4:
                return True
            i -= 1
            j += 1
        return False

    def __check_win_condition(self, col: int, marker: int):
        if self.__check_vertical(col, marker):
            return True
        if self.__check_horizontal(col, marker):
            return True
        if self.__check_left_diagonal(col, marker):
            return True
        if self.__check_right_diagonal(col, marker):
            return True

        return False

    def play(self, col: int, marker: int):
        if not self.is_legal(col):
            return ILLEGAL_MOVE

        if self.__drop_marker(col, marker):
            if self.__check_column_full(col):
                self.col_full[col] = True
            if self.__check_win_condition(col, marker):
                return WINNER
            return NO_WINNER

    def set_board(self, board):
        self.board = board

    def set_col_full(self, col_full):
        self.col_full = col_full

    def get_board_deepcopy(self):
        return copy.deepcopy(self.board)

    def get_col_full_deepcopy(self):
        return copy.deepcopy(self.col_full)

