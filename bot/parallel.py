from Board import Board
from common import *
from minmax import *
import pickle
def get_possible_game_states(depth, board, pieces_dictionary, board_states, turn_color, pieces_on_board_dict):
    if(depth == 0 or check_winner_efficient(board, pieces_dictionary[WHITE], pieces_dictionary[BLACK])):
        return;
    
    board_states.append([board, turn_color])
    pieces_on_board = pieces_on_board_dict[turn_color]
    valid_moves = get_valid_moves(board, turn_color, pieces_on_board)
    next_turn_color = WHITE
    if(turn_color == WHITE):
        next_turn_color = BLACK
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
        get_possible_game_states(depth - 1, board, pieces_dictionary, board_states, next_turn_color, pieces_on_board_dict)
        pieces_dictionary[turn_color].pop()
        account_for_push_moves_after(board, pieces_dictionary, push_moves)
        
        unmove(board, push_moves, move)
        # if(board != original_board):
        #     print("ur a dumbass")
        if(added_piece):
            pieces_on_board -= 1
            pieces_on_board_dict[turn_color] -= 1
    
def main():
    initial_board = []
    for i in range(0, BOARD_SIZE):
        row = [0] * 8
        initial_board.append(row)
    my_board = Board()
    my_board.from_2d_array(initial_board);
    board_states = []
    pieces_dictionary = {}
    pieces_dictionary[WHITE] = []
    pieces_dictionary[BLACK] = []
    pieces_on_board_dict = {}
    pieces_on_board_dict[WHITE] = 0
    pieces_on_board_dict[BLACK] = 0
    game_state_depth = 2
    get_possible_game_states(game_state_depth, my_board, pieces_dictionary, board_states,WHITE, pieces_on_board_dict)
    result = {}
    for i in range(0, len(board_states)):
        #game_states[i] = [Board obj, turn (-1, 1)]
        my_byte_array = board_states[i][0].board
        number_bytes = board_states[i][1].to_bytes(1, byteorder='big', signed=True)
        my_byte_array.extend(number_bytes)
        game_state_key = bytes(my_byte_array)
        turn_color = board_states[i][1]
        maximizing_player = True
        pieces_on_board_dict = get_piece_count_dict(my_board)
        maximizing_color = turn_color
        ##### MODIFY BELOW #####

        # Move logic should go here
        # This is where you'd call your minimax/MCTS/neural network/etc
        print(game_state_key)
        pieces_dictionary = retrieve_pieces_dictionary(my_board)
        value, move = min_max(my_board, turn_color, DEPTH, maximizing_player, pieces_on_board_dict, maximizing_color, ALPHA, BETA, pieces_dictionary)
        result[game_state_key] = move
    with open("data.pkl", "wb") as f:
        pickle.dump(result, f)
    

if __name__ == "__main__":
    main()

    

                
    