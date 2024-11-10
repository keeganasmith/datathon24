import math
import Board
import pickle
BADASS_TABLE = {}

ALPHA = -math.inf
BETA = math.inf
DEPTH = 3

WHITE = 1
BLACK = -1
EMPTY = 0

PIECES_PER_PLAYER = 8
BOARD_SIZE = 8

class Move:
    def __init__(self, r0 = None, c0 = None, r1 = None, c1 = None):
        if(r1 == None and c1 == None):
            raise Exception("invalid move, no target specified")
        self.r0 = r0
        self.c0 = c0
        self.r1 = r1
        self.c1 = c1
    def __str__(self):
        return f"start square: {self.r0}, {self.c0}\nend square: {self.r1}, {self.c1}\n"
with open("data1.pkl", "rb") as f:
    BADASS_TABLE = pickle.load(f)
    

def get_square(board, row, col):
    #Shoudn't it be row >= BOARD_SIZE?
    if(row < 0 or col < 0 or row > BOARD_SIZE or col > BOARD_SIZE):
        return None
    
    return board.get_cell(row, col)

def get_valid_moves(board, turn_color, num_pieces_on_board):
    possible_moves = []
    only_place = False

    if(num_pieces_on_board < PIECES_PER_PLAYER):
        only_place = True

    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if(only_place and get_square(board, i, j) == EMPTY):
                possible_moves.append(Move(r1=i, c1 = j))

            elif((not only_place) and turn_color == get_square(board, i, j)):
                for k in range(-1, 1):
                    for l in range(-1, 1):
                        if(k == 0 and l ==0):
                            continue
                        
                        if(get_square(board, i + k, j + l) == EMPTY):
                            possible_moves.append(Move(r0 = i, c0 = j, r1 = k, c1 = l))

    return possible_moves

def _torus(r, c):
    rt = (r + BOARD_SIZE) % BOARD_SIZE
    ct = (c + BOARD_SIZE) % BOARD_SIZE
    return rt, ct

def push_neighbors(board, r0, c0):
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    push_moves = []

    for dr, dc in dirs:
        r1, c1 = _torus(r0 + dr, c0 + dc)

        if board.get_cell(r1, c1) != EMPTY:
            r2, c2 = _torus(r1 + dr, c1 + dc)

            if board.get_cell(r2, c2) == EMPTY:
                temp = board.get_cell(r1, c1)
                board.set_cell(r1, c1, board.get_cell(r2, c2))
                board.set_cell(r2, c2, temp)
                push_moves.append(Move(r0 = r2, c0 = c2, r1 = r1, c1 = c1))

    return push_moves

def make_soft_move(board, move):
    if(board.get_cell(move.r0, move.c0) == EMPTY):
        raise Exception("no piece here dumbass")
    
    board.set_cell(move.r1, move.c1, board.get_cell(move.r0, move.c0))
    board.set_cell(move.r0, move.c0, EMPTY)

def make_move(board, move, turn_color):
    if(move is None):
        print("why is move none?")

    if move.r0 is not None and move.c0 is not None: #moving a piece (not placing)
        board.set_cell(move.r0, move.c0, EMPTY)
    
    board.set_cell(move.r1, move.c1, turn_color)

    return push_neighbors(board, move.r1, move.c1)

def get_piece_count_dict(board):
    result = {}
    result[WHITE] = 0
    result[BLACK] = 0
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if(board.get_cell(i, j) != EMPTY):
                result[board.get_cell(i, j)] += 1

    return result

def unmove(board, push_moves, move):
    for my_move in push_moves:
        make_soft_move(board, my_move)
        
    reversed_move = Move(r0 = move.r1, c0 = move.c1, r1 = move.r0, c1 = move.c1)
    temp = board.get_cell(reversed_move.r0, reversed_move.c0)
    board.set_cell(reversed_move.r0, reversed_move.c0, EMPTY)

    if(reversed_move.r1 is None): #piece was moved from off the board
        return
    
    board.set_cell(reversed_move.r1, reversed_move.c1, temp)

def check_winner_for_color(board, pieces, color):
    for i in range(0, len(pieces)):
        start_row = pieces[i][0]
        start_col = pieces[i][1]
        #check up
        row, col = _torus(start_row -1, start_col)
        if(board.get_cell(row, col) == color):
            row, col = _torus(start_row + 1, start_col)
            if(board.get_cell(row, col) == color):
                return True
        
        #check horizontal
        row, col = _torus(start_row, start_col - 1)
        if(board.get_cell(row, col) == color):
            row, col = _torus(start_row, start_col + 1)
            if(board.get_cell(row, col) == color):
                return True
        #check left diagonal
        row, col = _torus(start_row-1, start_col - 1)
        if(board.get_cell(row, col) == color):
            row, col = _torus(start_row + 1, start_col + 1)
            if(board.get_cell(row, col) == color):
                return True
        #check right diagonal
        row, col = _torus(start_row-1, start_col + 1)
        if(board.get_cell(row, col) == color):
            row, col = _torus(start_row + 1, start_col - 1)
            if(board.get_cell(row, col) == color):
                return True
    return False

def check_winner_efficient(board, white_pieces, black_pieces):
    winners = []
    if(check_winner_for_color(board, white_pieces, WHITE)):
        winners.append(WHITE)
    if(check_winner_for_color(board, black_pieces, BLACK)):
        winners.append(BLACK)
    return winners


def convert_move_to_list(my_move):
    result = []
    if(my_move.r0 is None):
        result = [my_move.r1, my_move.c1]
    else:
        result = [my_move.r0, my_move.c0, my_move.r1, my_move.c1]
    return result

def retrieve_pieces_dictionary(board):
    result = {}
    result[WHITE] = []
    result[BLACK] = []
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            element = board.get_cell(i, j)
            if(element != EMPTY):
                result[element].append([i, j])
    return result
