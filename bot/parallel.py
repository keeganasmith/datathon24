from Board import Board
from common import *
from minmax import *
from mpi4py import MPI
from multiprocessing import Pool, cpu_count
import pickle

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Process ID (node number)
size = comm.Get_size()  # Total number of nodes
num_threads = 192
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


# def main():
#     initial_board = []
#     for i in range(0, BOARD_SIZE):
#         row = [0] * 8
#         initial_board.append(row)
#     my_board = Board()
#     my_board.from_2d_array(initial_board);
#     board_states = []
#     pieces_dictionary = {}
#     pieces_dictionary[WHITE] = []
#     pieces_dictionary[BLACK] = []
#     pieces_on_board_dict = {}
#     pieces_on_board_dict[WHITE] = 0
#     pieces_on_board_dict[BLACK] = 0
#     game_state_depth = 2
#     get_possible_game_states(game_state_depth, my_board, pieces_dictionary, board_states,WHITE, pieces_on_board_dict)
#     result = {}
#     for i in range(0, len(board_states)):
#         #game_states[i] = [Board obj, turn (-1, 1)]
#         my_byte_array = bytearray(board_states[i][0].board)
#         number_bytes = board_states[i][1].to_bytes(1, byteorder='big', signed=True)
#         my_byte_array.extend(number_bytes)
#         game_state_key = bytes(my_byte_array)
#         turn_color = board_states[i][1]
#         maximizing_player = True
#         pieces_on_board_dict = get_piece_count_dict(my_board)
#         maximizing_color = turn_color
#         ##### MODIFY BELOW #####

#         # Move logic should go here
#         # This is where you'd call your minimax/MCTS/neural network/etc
#         pieces_dictionary = retrieve_pieces_dictionary(my_board)
#         value, move = min_max(my_board, turn_color, DEPTH, maximizing_player, pieces_on_board_dict, maximizing_color, ALPHA, BETA, pieces_dictionary)
#         result[game_state_key] = move
#     with open("data.pkl", "wb") as f:
#         pickle.dump(result, f)



# Function to process a single board state
def process_board_state(board_state, my_board):
    # my_byte_array = bytearray(board_state[0].board)
    # number_bytes = board_state[1].to_bytes(1, byteorder='big', signed=True)
    # my_byte_array.extend(number_bytes)
    # game_state_key = bytes(my_byte_array)
    game_state_key = board_state[0].to_string()
    game_state_key += str(board_state[1])
    turn_color = board_state[1]
    maximizing_player = True
    pieces_on_board_dict = get_piece_count_dict(board_state[0])
    maximizing_color = turn_color
    
    # Call the minimax function or another AI method
    pieces_dictionary = retrieve_pieces_dictionary(board_state[0])
    value, move = min_max(board_state[0], turn_color, DEPTH, maximizing_player, pieces_on_board_dict,
                          maximizing_color, ALPHA, BETA, pieces_dictionary)
    print("finished game state")
    return game_state_key, move

def main():
    # Initialize board and setup state
    initial_board = []
    for i in range(0, BOARD_SIZE):
        row = [0] * 8
        initial_board.append(row)
    
    my_board = Board()
    my_board.from_2d_array(initial_board)

    board_states = []
    pieces_dictionary = {WHITE: [], BLACK: []}
    pieces_on_board_dict = {WHITE: 0, BLACK: 0}

    # Generate possible game states
    game_state_depth = 3
    get_possible_game_states(game_state_depth, my_board, pieces_dictionary, board_states, WHITE, pieces_on_board_dict)
    print("finished retrieving possible game states")
    print("length of game states is, ", len(board_states))
    for i in range(0, len(board_states)):
        print(board_states[i].to_string())
    raise Exception("hello there")
    # Divide work among MPI processes
    total_board_states = len(board_states)
    local_start = (total_board_states // size) * rank
    local_end = (total_board_states // size) * (rank + 1)
    if rank == size - 1:
        local_end = total_board_states  # Last process handles any remainder
    
    # Process each board state in the local range
    with Pool(processes=num_threads) as pool:
        local_results = pool.starmap(process_board_state, [(board_states[i], my_board) for i in range(local_start, local_end)])

    # Convert local_results to a dictionary
    local_results_dict = {game_state_key: move for game_state_key, move in local_results} 
    # Gather results from all processes
    all_results = comm.gather(local_results, root=0)

    # Combine results in the root process and save to file
    if rank == 0:
        final_results = {}
        for result in all_results:
            final_results.update(result)
        with open("data1.pkl", "wb") as f:
            pickle.dump(final_results, f)

if __name__ == "__main__":
    main()



    

                
    
