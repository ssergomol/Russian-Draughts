import numpy as np
from typing import Optional, List


def sign(item):
    if item > 0:
        return 1
    elif item < 0:
        return -1
    else:
        return 0


class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player

    def inverted(self) -> 'BoardState':
        return BoardState(board=self.board[::-1, ::-1] * -1, current_player=self.current_player * -1)

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def do_move(self, from_x, from_y, to_x, to_y) -> Optional['BoardState']:
        """
        :return: new BoardState or None for invalid move
        """
        if (self.current_player > 0) != (self.board[from_y, from_x] > 0):
            result = self.copy()
            return result
        if from_x == to_x and from_y == to_y:
            return None

        if (to_x + to_y) % 2 == 0:
            return None
        ate = False
        dis_x = to_x - from_x
        dis_y = to_y - from_y
        result = self.copy()
        if abs(self.board[from_y, from_x]) == 1:
            if abs(dis_x) == 2:
                ate = True
                new_y = int(from_y + (dis_y / 2))
                new_x = int(from_x + (dis_x / 2))
                result.board[new_y, new_x] = 0
            result.board[to_y, to_x] = result.board[from_y, from_x]
            result.board[from_y, from_x] = 0
        if abs(self.board[from_y, from_x]) == 2:
            x_ = from_x
            y_ = from_y
            for i in range(abs(dis_x)):
                x_ += int(abs(dis_x) / dis_x)
                y_ += int(abs(dis_y) / dis_y)
                if abs(self.board[y_, x_]) != 0:
                    result.board[y_, x_] = 0
                    ate = True
            result.board[to_y, to_x] = result.board[from_y, from_x]
            result.board[from_y, from_x] = 0
        if self.current_player == 1 and to_y == 0:
            result.board[to_y, to_x] = 2
        elif self.current_player == -1 and to_y == 7:
            result.board[to_y, to_x] = -2

        if not ate:
            result.current_player *= -1
        return result

    def queen_possible_moves(self, pos_x, pos_y):
        possible_moves = []
        if sign(self.current_player) != sign(self.board[pos_y, pos_x]):
            return possible_moves
        for k in range(4):
            ate_flag = 0
            i = pos_y
            j = pos_x
            first = 1
            second = 1
            if k == 1:
                first = -1
            elif k == 2:
                second = -1
            elif k == 3:
                first = -1
                second = -1
            while 0 <= i <= 7 and 0 <= j <= 7:
                i += first
                j += second
                if i > 7 or j > 7 or i < 0 or j < 0:
                    break
                if sign(self.board[i, j]) == sign(self.current_player):
                    break
                if sign(self.board[i, j]) \
                        != sign(self.current_player) and sign(self.board[i, j]) != 0:
                    ate_flag += 1
                    continue
                if ate_flag <= 1:
                    possible_moves.append((i, j))
        return possible_moves

    def get_possible_moves(self, pos_x, pos_y):
        possible_moves = []

        if sign(self.current_player) != sign(self.board[pos_y, pos_x]):
            return possible_moves
        if pos_y % 2 != pos_x % 2:
            fl = self.board[pos_y, pos_x]
            for i in range(pos_y - 1, pos_y + 2):
                for j in range(pos_x - 1, pos_x + 2):
                    if i > 7 or i < 0 or j > 7 or j < 0:
                        continue
                    if self.board[i, j] == fl or self.board[i, j] == 2 * fl:
                        continue
                    if (i % 2) != (j % 2) and self.board[i, j] == 0:
                        possible_moves.append((i, j))
                    if self.board[i, j] == -fl or self.board[i, j] == -2 * fl:
                        differ_i = i - pos_y
                        differ_j = j - pos_x
                        new_i = i + differ_i
                        new_j = j + differ_j
                        if 7 >= new_i >= 0 and 7 >= new_j >= 0:
                            if self.board[new_i, new_j] == 0:
                                possible_moves.append((new_i, new_j))

        return possible_moves

    @property
    def is_game_finished(self) -> bool:
        ...  # todo

    @property
    def get_winner(self) -> Optional[int]:
        ...  # todo

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(8, 8), dtype=np.int8)
        for i in range(3):
            for j in range(8):
                if (i % 2) != (j % 2):
                    board[i, j] = -1
                if ((7 - i) % 2) != (j % 2):
                    board[7 - i, j] = 1
        return BoardState(board, 1)
