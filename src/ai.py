from typing import Optional
import random
from .boardstate import BoardState


def sign(item):
    if item > 0:
        return 1
    elif item < 0:
        return -1
    else:
        return 0


def total_evaluation(board: BoardState):
    evaluation = 0
    for i in range(8):
        for j in range(8):
            if abs(board.board[i, j]) == 2:
                evaluation += board.board[i, j] * 5
            else:
                evaluation += board.board[i, j]
    return evaluation


def ai_evaluation(board: BoardState):
    evaluation = 0
    for i in range(8):
        for j in range(8):
            if abs(board.board[i, j]) == 2:
                evaluation += abs(board.board[i, j] * 5)
            else:
                evaluation += abs(board.board[i, j])
    return evaluation


def player_evaluation(board: BoardState):
    evaluation = 0
    for i in range(8):
        for j in range(8):
            if board.board[i, j] > 0:
                if abs(board.board[i, j]) == 2:
                    evaluation += board.board[i, j] * 5
                else:
                    evaluation += board.board[i, j]
    return evaluation


min_move = 0
best_move = 0
flag = False


class AI:
    def __init__(self, search_depth: int):
        self.depth: int = search_depth
        self.from_x = 7
        self.from_y = 2
        self.to_x = 6
        self.to_y = 3

    def random_func(self, all_possible_pawns, board: BoardState):
        index = random.randint(0, len(all_possible_pawns) - 1)
        first = all_possible_pawns[index]
        self.from_y = first[0]
        self.from_x = first[1]
        all_moves = board.get_possible_moves(self.from_x, self.from_y)
        index_second = random.randint(0, len(all_moves) - 1)
        second = all_moves[index_second]
        self.to_y = second[0]
        self.to_x = second[1]

    def pos_eval_func(self, board: BoardState, depth):
        global min_move
        global flag
        global best_move
        all_possible_pawns = []
        if depth == 0:
            return total_evaluation(board)
        for i in range(8):
            for j in range(8):
                if sign(board.board[i, j]) == sign(board.current_player):
                    moves = []
                    if abs(board.board[i, j]) == 1:
                        moves = board.get_possible_moves(j, i)
                        if len(moves) == 0:
                            continue
                    elif abs(board.board[i, j]) == 2:
                        moves = board.queen_possible_moves(j, i)
                        if len(moves) == 0:
                            continue
                    if len(moves) == 0:
                        continue
                    all_possible_pawns.append((i, j))
                    for move in moves:
                        temp_board = board.copy()
                        temp_board = temp_board.do_move(j, i, move[1], move[0])
                        current_evaluation = total_evaluation(temp_board)
                        best_evaluation = self.pos_eval_func(temp_board, depth - 1)
                        best_move = min(current_evaluation, best_evaluation)
                        if not flag:
                            if current_evaluation < 0:
                                self.from_y = i
                                self.from_x = j
                                self.to_y = move[0]
                                self.to_x = move[1]
                                min_move = current_evaluation
                                flag = True
                            else:
                                self.random_func(all_possible_pawns, board)
                                flag = True
                        if depth == self.depth:
                            if current_evaluation < min_move:
                                self.from_y = i
                                self.from_x = j
                                self.to_y = move[0]
                                self.to_x = move[1]
                                min_move = current_evaluation
                            else:
                                self.random_func(all_possible_pawns, board)
        return best_move

