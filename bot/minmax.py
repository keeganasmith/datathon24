import math
from common import *
from evaluate import *
import copy

def min_max(board, turn_color, depth, maximizing_player, pieces_on_board_dict, maximizing_color):
    if depth == 0 or len(check_winner(board)) != 0:
        opposite_color = white
        if(maximizing_color == white):
            opposite_color = black
        my_heuristic = heuristic(board, maximizing_color)
        other_heuristic = heuristic(board, opposite_color)
        if(my_heuristic == math.inf and other_heuristic == math.inf):
            if(turn_color == opposite_color):
                return math.inf, None
            return -math.inf, None
        return (my_heuristic - other_heuristic), None
    
    pieces_on_board = pieces_on_board_dict[turn_color]
    valid_moves = get_valid_moves(board, turn_color, pieces_on_board)
    next_turn_color = white
    if(turn_color == white):
        next_turn_color = black
    if(maximizing_player):
        max_value = -math.inf
        best_move = None;
        for move in valid_moves:
            added_piece = False
            #original_board = copy.deepcopy(board)
            push_moves = make_move(board, move, turn_color)
            if(pieces_on_board_dict[turn_color] < BOARD_SIZE):
                pieces_on_board += 1
                pieces_on_board_dict[turn_color] += 1
                added_piece = True
            value, _garb = min_max(board, next_turn_color, depth-1, not maximizing_player, pieces_on_board_dict, maximizing_color)
            if(value > max_value):
                max_value = value
                best_move = move
            unmove(board, push_moves, move)
            # if(board != original_board):
            #     print("ur a dumbass")
            if(added_piece):
                pieces_on_board -= 1
                pieces_on_board_dict[turn_color] -= 1
        if best_move is None:
            best_move = valid_moves[0]
        return max_value, best_move
    else:
        min_value = math.inf
        for move in valid_moves:
            added_piece = False
            #original_board = copy.deepcopy(board)
            push_moves = make_move(board, move, turn_color)
            if(pieces_on_board_dict[turn_color] < BOARD_SIZE):
                pieces_on_board += 1
                pieces_on_board_dict[turn_color] += 1
                added_piece = True
            value, _garb = min_max(board, next_turn_color, depth-1, not maximizing_player, pieces_on_board_dict, maximizing_color)
            min_value = min(value, min_value)
            unmove(board, push_moves, move)
            # if(board != original_board):
            #     print("ur a dumbass")
            if(added_piece):
                pieces_on_board -= 1
                pieces_on_board_dict[turn_color] -= 1
        return min_value, None
def display_board(board):
    for i in range(0, len(board)):
        row = ""
        for j in range(0, len(board)):
            row += board[i][j] + " "
        print(row)

def main():
    board = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    turn_color = "W"
    depth = 3
    maximizing_player = "W"
    pieces_on_board_dict = get_piece_count_dict(board)
    value, best_move = min_max(board, turn_color, depth, maximizing_player, pieces_on_board_dict, maximizing_player)
    print("best move score: ", value)
    make_move(board, best_move, turn_color)
    display_board(board)
    while(True):
        if(turn_color == white):
            turn_color = black
        else:
            turn_color = white

        maximizing_player= turn_color
        pieces_on_board_dict = get_piece_count_dict(board)
        value, best_move = min_max(board, turn_color, depth, maximizing_player, pieces_on_board_dict, maximizing_player)
        make_move(board, best_move, turn_color)
        print("best move score: ", value)
        print("turn is ", turn_color)
        print("move is ", best_move)
        display_board(board)
        print()
        print()
        if(len(check_winner(board)) != 0):
            break;
    

if __name__ == "__main__":
    main()
        

            


    

                
    