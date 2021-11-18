# Min-Max Algorithm
from math import inf as infinity
from random import choice
import platform
from os import system
import time
import numpy as np

playersym_arr = ['X', 'O']
HUMAN = -1
COMP = +1
board = np.zeros((3, 3), dtype=np.int32)


# board = [[-1, -1, 1], [0, 1, 0], [-1, 1, 0]] alpha beta pruning test conditions

# checking from current who wins
def evaluate(curr_state):
    if wins(curr_state, COMP):
        score = +1
    elif wins(curr_state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(curr_board, player_value):
    win_state = [
        [curr_board[0][0], curr_board[1][1], curr_board[2][2]],  # diagonal
        [curr_board[2][0], curr_board[1][1], curr_board[0][2]],  # diagonal
        [curr_board[0][0], curr_board[0][1], curr_board[0][2]],  # horizontal
        [curr_board[1][0], curr_board[1][1], curr_board[1][2]],  # horizontal
        [curr_board[2][0], curr_board[2][1], curr_board[2][2]],  # horizontal
        [curr_board[0][0], curr_board[1][0], curr_board[2][0]],  # vertical
        [curr_board[0][1], curr_board[1][1], curr_board[2][1]],  # vertical
        [curr_board[0][2], curr_board[1][2], curr_board[2][2]],  # vertical
    ]
    if [player_value, player_value, player_value] in win_state:
        return True
    else:
        return False


# to check if game overs, use wins function to check all winning conditions
def game_over(curr_board):
    if wins(curr_board, HUMAN):  # Human wins
        return True
    elif wins(curr_board, COMP):  # Computer wins
        return True
    else:  # No one has won yet
        return False


def empty_cells(curr_board):
    cells_list = []
    for r, row in enumerate(curr_board):
        for c, cell in enumerate(row):
            if cell == 0:
                cells_list.append([r, c])

    return cells_list  # return all empty cell positions list


def valid_move(r, c):
    if [r, c] in empty_cells(board):  # move is only valid if that place in the board is empty, no other restriction
        return True
    else:
        return False


def set_move(r, c, player_symbol):  # put player symbol on the selected board cell
    board[r][c] = player_symbol


def boardprint(a, b):  # for testing alpha beta pruning # hardcoded for symbols
    print("\n \n")
    for r in board:
        for c in r:
            if c == 1:
                print('X', end=" ")
            elif c == -1:
                print('O', end=" ")
            else:
                print('-', end=" ")

        print()
    print("Alpha : ", a)
    print("Beta  : ", b)


def alphabeta(curr_board, depth, player, alpha, beta):
    if player == COMP:
        best = [-1, -1, -99]
    else:
        best = [-1, -1, +99]

    if alpha >= beta or depth == 0 or game_over(curr_board):  # if board is not empty or game is over # reached the
        # terminals
        score = evaluate(curr_board)
        return [-1, -1, score]

    for cell in empty_cells(curr_board):
        r, c = cell[0], cell[1]  # get empty pos
        curr_board[r][c] = player  # put computer symbol in that empty position
        score = alphabeta(curr_board, depth - 1, -player, alpha,
                          beta)  # run alpha-beta algorithm on the new state of the board
        # for the next  player
        curr_board[r][c] = 0  # get back to the previous state of the board
        score[0] = r  # the row value
        score[1] = c  # the column value

        if player == COMP:  # maximum level
            if score[2] > alpha:  # node value greater than alpha than update alpha
                alpha = score[2]
                best = score
        else:  # minimum level
            if score[2] < beta:  # node value less than beta than update beta
                beta = score[2]
                best = score

    return best  # r, c, score


# clean the window
def clean():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def printBoard(curr_board, comp_choice, human_choice):
    chars = {
        -1: human_choice,
        +1: comp_choice,
        0: ' '
    }
    str_line = '---------------'
    print('\n' + str_line)
    for row in curr_board:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def computer_turn(comp_choice, human_choice):
    empty_pos = len(empty_cells(board))
    if empty_pos == 0 or game_over(board):  # if there are no more empty positions or game is over then return
        return

    print(f'Computer turn [{comp_choice}]')
    printBoard(board, comp_choice, human_choice)
    alpha = -infinity
    beta = +infinity
    if empty_pos == 9:  # if board is empty, hardcoded middle box
        x = 1
        y = 1
    else:  # if board is not empty , use minimax algorithm to get position
        move = alphabeta(board, empty_pos, COMP, alpha, beta)
        x, y = move[0], move[1]
    if valid_move(x, y):
        set_move(x, y, COMP)


def human_turn(c_choice, h_choice):
    move = -1
    moves = {  # all the positions assigned by 1 to 9
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    print(f'Human turn [{h_choice}]')
    printBoard(board, c_choice, h_choice)

    while move < 1 or move > 9:
        move = int(input('Select Empty Cell from 1 to 9: '))
        row = moves[move][0]  # row position of the board
        column = moves[move][1]  # column position of the board
        if valid_move(row, column):  # check if the move is valid
            set_move(row, column, HUMAN)  # if move is valid, set the symbol there
        else:
            print('Select Valid Cell')  # if move was not valid, ask again the move


def get_human_symbol():
    human_choice = ''
    while human_choice not in playersym_arr:
        human_choice = input('Choose X or O\nChosen: ').upper()
    return human_choice


def get_computer_symbol(h_choice):
    if h_choice == playersym_arr[0]:
        return playersym_arr[1]
    else:
        return playersym_arr[0]


def print_result(comp_choice, human_choice):
    clean()
    printBoard(board, comp_choice, human_choice)
    if wins(board, HUMAN):
        print('HUMAN WIN !!!')
    elif wins(board, COMP):
        print('COMPUTER WIN !!!')
    else:
        print('DRAW !!!')


def main():
    clean()
    h_choice = ''
    c_choice = ''
    first = ''  # if human is the first
    h_choice = get_human_symbol()
    c_choice = get_computer_symbol(h_choice)

    clean()
    while first != 'Y' and first != 'N':
        first = input('You want to Start First ?[Y/N]: ').upper()

    if first == 'N':  # if computer is making the first move
        computer_turn(c_choice, h_choice)
        first = ''

    while len(empty_cells(board)) > 0 and not game_over(board):  # till someone wins or game draws
        human_turn(c_choice, h_choice)
        computer_turn(c_choice, h_choice)

    print_result(c_choice, h_choice)

    exit()


if __name__ == '__main__':
    main()
