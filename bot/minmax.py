import math
from common import *
from evaluate import *
import copy
def index_of(pieces, target):
    for i in range(0, len(pieces)):
        if(pieces[i] == target):
            return i
    return -1
def account_for_push_moves(board, piece_dictionary, push_moves):
    for move in push_moves:
        color = board.get_cell(move.r0, move.c0)
        index = index_of(piece_dictionary[color], [move.r1, move.c1])
        piece_dictionary[color][index] = [move.r0, move.c0]

def account_for_push_moves_after(board, piece_dictionary, push_moves):
     for move in push_moves:
        color = board.get_cell(move.r0, move.c0)
        index = index_of(piece_dictionary[color], [move.r0, move.c0])
        piece_dictionary[color][index] = [move.r1, move.c1]
def check_if_in_board_state(board, turn_color):
    game_state_key = board.to_string()
    game_state_key += str(turn_color)
    move = BADASS_TABLE.get(game_state_key, None)
    return move

def min_max(board, turn_color, depth, maximizing_player, pieces_on_board_dict, maximizing_color, alpha, beta, pieces_dictionary, first = True):
    if(first):
        move = check_if_in_board_state(board, turn_color)
        if(move):
            return None, move
        first = False
    if depth == 0 or len(check_winner_efficient(board, pieces_dictionary[WHITE], pieces_dictionary[BLACK])) != EMPTY:
        opposite_color = WHITE
        if(maximizing_color == WHITE):
            opposite_color = BLACK
        my_heuristic = heuristic(board, maximizing_color, pieces_dictionary[maximizing_color]) # this shit might not work
        other_heuristic = heuristic(board, opposite_color, pieces_dictionary[opposite_color])
        if(my_heuristic == math.inf and other_heuristic == math.inf):
            if(turn_color == opposite_color):
                return math.inf, None
            return -math.inf, None
        return (my_heuristic - other_heuristic), None
    
    pieces_on_board = pieces_on_board_dict[turn_color]
    valid_moves = get_valid_moves(board, turn_color, pieces_on_board)
    next_turn_color = WHITE
    if(turn_color == WHITE):
        next_turn_color = BLACK
    if(maximizing_player):
        max_value = -math.inf
        best_move = None
        for move in valid_moves:
            added_piece = False
            #original_board = copy.deepcopy(board)
            push_moves = make_move(board, move, turn_color)
            if(pieces_on_board_dict[turn_color] < BOARD_SIZE):
                pieces_on_board += 1
                pieces_on_board_dict[turn_color] += 1
                added_piece = True
            account_for_push_moves(board, pieces_dictionary, push_moves)
            if(not (move.r0 is None)):
                index = index_of(pieces_dictionary[turn_color], [move.r0, move.c0])
                del pieces_dictionary[turn_color][index]
            pieces_dictionary[turn_color].append([move.r1, move.c1])
            value, _garb = min_max(board, next_turn_color, depth-1, not maximizing_player, pieces_on_board_dict, maximizing_color, alpha, beta, pieces_dictionary)
            pieces_dictionary[turn_color].pop()
            account_for_push_moves_after(board, pieces_dictionary, push_moves)
            if(value > max_value):
                max_value = value
                best_move = move
            
            unmove(board, push_moves, move)
            # if(board != original_board):
            #     print("ur a dumbass")
            if(added_piece):
                pieces_on_board -= 1
                pieces_on_board_dict[turn_color] -= 1
            if(max_value > beta):
                break
            alpha = max(alpha, max_value)
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
            account_for_push_moves(board, pieces_dictionary, push_moves)

            if(not (move.r0 is None)):
                index = index_of(pieces_dictionary[turn_color], [move.r0, move.c0])
                del pieces_dictionary[turn_color][index]
            pieces_dictionary[turn_color].append([move.r1, move.c1])
            value, _garb = min_max(board, next_turn_color, depth-1, not maximizing_player, pieces_on_board_dict, maximizing_color, alpha, beta, pieces_dictionary)
            pieces_dictionary[turn_color].pop()
            account_for_push_moves_after(board, pieces_dictionary, push_moves)
            min_value = min(value, min_value)
            
            unmove(board, push_moves, move)
            # if(board != original_board):
            #     print("ur a dumbass")
            if(added_piece):
                pieces_on_board -= 1
                pieces_on_board_dict[turn_color] -= 1
            if(min_value < alpha):
                break
            beta = min(beta, min_value)
        return min_value, None
def display_board(board):
    for i in range(0, len(board)):
        row = ""
        for j in range(0, len(board)):
            row += board.get_cell(i, j) + " "
        print(row)


            


    

                
    