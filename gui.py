from itertools import product

import pygame
from pygame import Surface
from src.ai import AI
from src.boardstate import BoardState
import pickle

may_be_eaten_and_ate = False
pos_x_eaten = 0
pos_y_eaten = 0


def draw_board(screen: Surface, pos_x: int, pos_y: int, elem_size: int, board: BoardState):
    dark = (0, 0, 0)
    white = (200, 200, 200)

    for y, x in product(range(8), range(8)):
        color = white if (x + y) % 2 == 0 else dark
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        pygame.draw.rect(screen, color, position)

        figure = board.board[y, x]

        if figure == 0:
            continue

        if figure > 0:
            figure_color = 255, 255, 255
        else:
            figure_color = 100, 100, 100
        r = elem_size // 2 - 10

        pygame.draw.circle(screen, figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)
        if abs(figure) == 2:
            r = 5
            negative_color = [255 - e for e in figure_color]
            pygame.draw.circle(screen, negative_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)


def game_loop(screen: Surface, board: BoardState, ai: AI):
    grid_size = screen.get_size()[0] // 8

    while True:

        draw_board(screen, 0, 0, grid_size, board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_position = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                global may_be_eaten_and_ate, pos_y_eaten, pos_x_eaten
                new_x, new_y = [p // grid_size for p in event.pos]
                old_x, old_y = [p // grid_size for p in mouse_click_position]
                if may_be_eaten_and_ate and old_x == pos_x_eaten and old_y == pos_y_eaten and abs(new_x - old_x > 1):
                    board.current_player *= -1
                    possible_move = board.possible_move_val_for_eaten(old_y, old_x, new_y, new_x)
                    new_board = board.do_move(old_x, old_y, new_x, new_y)
                    if board.can_eat(new_x, new_y):
                        may_be_eaten_and_ate = True
                        pos_y_eaten = new_y
                        pos_x_eaten = new_x
                    else:
                        may_be_eaten_and_ate = False
                    if new_board is not None and possible_move:
                        board = new_board
                    board.current_player *= -1
                if not may_be_eaten_and_ate:
                    if old_x == new_x and old_y == new_y:
                        board.cell_highlighting(old_x, old_y, new_x, new_y, grid_size, screen)
                    else:
                        possible_move = board.possible_move_val(old_y, old_x, new_y, new_x)
                        new_board = board.do_move(old_x, old_y, new_x, new_y)
                        if new_board is not None and possible_move:
                            board = new_board
                        if abs(new_x - old_x) > 1 and board.can_eat(new_x, new_y):
                            may_be_eaten_and_ate = True
                            pos_y_eaten = new_y
                            pos_x_eaten = new_x
                        else:
                            may_be_eaten_and_ate = False
                        board.current_player *= -1

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                x, y = [p // grid_size for p in event.pos]
                board.board[y, x] = (board.board[y, x] + 1 + 2) % 5 - 2  # change figure
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = board.inverted()
                if event.key == pygame.K_SPACE:
                    if board.current_player == -1:
                        while board.current_player == -1:
                            ai.pos_eval_func(board, ai.depth)
                            new_board = board.do_move(ai.from_x, ai.from_y, ai.to_x, ai.to_y)
                            if new_board is not None:
                                board = new_board
                            if abs(ai.from_x - ai.to_x) > 1 and board.can_eat(ai.to_x, ai.to_y):
                                board = board.ai_do_move_and_eat(ai.to_x, ai.to_y)
                            board.current_player *= -1

                if event.key == pygame.K_s:
                    with open("save", "wb") as b:
                        pickle.dump(board, b)
                if event.key == pygame.K_l:
                    with open("save", "rb") as b:
                        board = pickle.load(b)

            pygame.display.flip()


pygame.init()

screen: Surface = pygame.display.set_mode([512, 512])

ai = AI(search_depth=3)
pygame.display.update()
game_loop(screen, BoardState.initial_state(), ai)

pygame.quit()
