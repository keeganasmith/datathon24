import math
ALPHA = -math.inf
BETA = math.inf
DEPTH = 3
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
white_piece = "W"
black_pieve = "B"
white = "W"
black = "B"
empty = "."
PIECES_PER_PLAYER = 8
BOARD_SIZE = 8
def get_square(board, row, col):
    if(row < 0 or col < 0 or row > len(board) or col > len(board[0])):
        return None
    return board[row][col]
def get_valid_moves(board, turn_color, num_pieces_on_board):
    possible_moves = []
    only_place = False
    if(num_pieces_on_board < PIECES_PER_PLAYER):
        only_place = True
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if(only_place and get_square(board, i, j) == empty):
                possible_moves.append(Move(r1=i, c1 = j))
            elif((not only_place) and turn_color == get_square(board, i, j)):
                for k in range(-1, 1):
                    for l in range(-1, 1):
                        if(k == 0 and l ==0):
                            continue;
                        if(get_square(board, i + k, j + l) == empty):
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
        if board[r1][c1] != empty:
            r2, c2 = _torus(r1 + dr, c1 + dc)
            if board[r2][c2] == empty:
                board[r2][c2], board[r1][c1] = board[r1][c1], board[r2][c2]
                push_moves.append(Move(r0 = r2, c0 = c2, r1 = r1, c1 = c1))
    return push_moves
def make_soft_move(board, move):
    if(board[move.r0][move.c0] == empty):
        raise Exception("no piece here dumbass")
    
    board[move.r1][move.c1] = board[move.r0][move.c0]
    board[move.r0][move.c0] = empty
def make_move(board, move, turn_color):
    if(move is None):
        print("why is move noen?")
    if move.r0 is not None and move.c0 is not None: #moving a piece (not placing)
        board[move.r0][move.c0] = "."
    
    board[move.r1][move.c1] = turn_color
    return push_neighbors(board, move.r1, move.c1)
def get_piece_count_dict(board):
    result = {}
    result[white] = 0
    result[black] = 0
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if(board[i][j] != empty):
                result[board[i][j]] += 1
    return result
def unmove(board, push_moves, move):
    for my_move in push_moves:
        make_soft_move(board, my_move)
    reversed_move = Move(r0 = move.r1, c0 = move.c1, r1 = move.r0, c1 = move.c1)
    temp = board[reversed_move.r0][reversed_move.c0]
    board[reversed_move.r0][reversed_move.c0] = empty

    if(reversed_move.r1 is None): #piece was moved from off the board
        return
    
    board[reversed_move.r1][reversed_move.c1] = temp

def check_winner_for_color(board, pieces, color):
    for i in range(0, len(pieces)):
        start_row = pieces[i][0]
        start_col = pieces[i][1]
        #check up
        row, col = _torus(start_row -1, start_col)
        if(board[row][col] == color):
            row, col = _torus(start_row + 1, start_col)
            if(board[row][col] == color):
                return True
        
        #check horizontal
        row, col = _torus(start_row, start_col - 1)
        if(board[row][col] == color):
            row, col = _torus(start_row, start_col + 1)
            if(board[row][col] == color):
                return True
        #check left diagonal
        row, col = _torus(start_row-1, start_col - 1)
        if(board[row][col] == color):
            row, col = _torus(start_row + 1, start_col + 1)
            if(board[row][col] == color):
                return True;
        #check right diagonal
        row, col = _torus(start_row-1, start_col + 1)
        if(board[row][col] == color):
            row, col = _torus(start_row + 1, start_col - 1)
            if(board[row][col] == color):
                return True;
    return False

def check_winner_efficient(board, white_pieces, black_pieces):
    winners = []
    if(check_winner_for_color(board, white_pieces, white)):
        winners.append(white)
    if(check_winner_for_color(board, black_pieces, black)):
        winners.append(black)
    return winners


        
def check_winner(board):
    white_wins = False
    black_wins = False
    # check rows
    for row in range(0, BOARD_SIZE):
        cnt = 0
        tile = empty
        for col in range(-2, BOARD_SIZE+2):
            r, c = _torus(row, col)
            curr_tile = board[r][c]
            if curr_tile == empty:
                cnt = 0
            elif curr_tile != tile:
                cnt = 1
            else:
                cnt += 1
                if (cnt == 3):
                    if tile == white:
                        white_wins = True
                    elif tile == black:
                        black_wins = True
            tile = board[r][c]

    # check cols
    for col in range(0, BOARD_SIZE):
        cnt = 0
        tile = empty
        for row in range(-2, BOARD_SIZE+2):
            r, c = _torus(row, col)
            curr_tile = board[r][c]
            if curr_tile == empty:
                cnt = 0
            elif curr_tile != tile:
                cnt = 1
            else:
                cnt += 1
                if (cnt == 3):
                    if tile == white:
                        white_wins = True
                    elif tile == black:
                        black_wins = True
            tile = board[r][c]

    # check negative diagonals
    for col_start in range(0, BOARD_SIZE):
        cnt = 0
        tile = empty
        for i in range(-2, BOARD_SIZE+2):
            r, c = _torus(i, col_start + i)
            curr_tile = board[r][c]
            if curr_tile == empty:
                cnt = 0
            elif curr_tile != tile:
                cnt = 1
            else:
                cnt += 1
                if (cnt == 3):
                    if tile == white:
                        white_wins = True
                    elif tile == black:
                        black_wins = True
            tile = board[r][c]

    # check positive diagonals
    for col_start in range(0, BOARD_SIZE):
        cnt = 0
        tile = empty
        for i in range(-2, BOARD_SIZE+2):
            r, c = _torus(i, col_start - i)
            curr_tile = board[r][c]
            if curr_tile == empty:
                cnt = 0
            elif curr_tile != tile:
                cnt = 1
            else:
                cnt += 1
                if (cnt == 3):
                    if tile == white:
                        white_wins = True
                    elif tile == black:
                        black_wins = True
            tile = board[r][c]

    if white_wins and black_wins:
        return [white, black]
    # If only one player has 3 in a row, they win
    elif white_wins:
        return [white]
    elif black_wins:
        return [black]

    return [] # no one has won the game 

def convert_move_to_list(my_move):
    result = []
    if(my_move.r0 is None):
        result = [my_move.r1, my_move.c1]
    else:
        result = [my_move.r0, my_move.c0, my_move.r1, my_move.c1]
    return result

def retrieve_pieces_dictionary(board):
    result = {}
    result[white] = []
    result[black] = []
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            element = board[i][j]
            if(element != empty):
                result[element].append([i, j])
    return result

def convert_from_input_board(board):
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if(board[i][j] == -1):
                board[i][j] = "B"
            if(board[i][j] == 0):
                board[i][j] = "."
            if(board[i][j] == 1):
                board[i][j] = "W"

def main():
    board = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'B', '.', '.', 'B', '.'],
    ['.', '.', 'B', 'B', 'B', '.', '.', '.'],
    ['.', '.', '.', 'B', '.', '.', '.', 'B'],
    ['.', '.', 'B', '.', 'B', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', 'B', '.', 'B', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    result = retrieve_pieces_dictionary(board)
    print(result)
if __name__ == "__main__":
    main()