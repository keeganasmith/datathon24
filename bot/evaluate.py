from common import *
import math
# board is a 8x8 2d array containing pieces that are either W, B, .
# turn_color is W or B

class Board:
    def __init__(self, size=8):
        """
        Initializes an 8x8 board represented as a bitmap.
        Each cell uses 2 bits: 00 for empty, 01 for black, 10 for white.
        """
        self.size = size
        self.board = bytearray(size * size * 2 // 8)

    def set_cell(self, row, col, value):
        """
        Sets the value at a given (row, col).
        Value should be 0 (empty), 1 (white), or -1 (black).
        """
        if value not in [-1, 0, 1]:
            raise ValueError("Invalid value. Must be 0 (empty), 1 (white), or -1 (black).")
        
        # Convert -1 (black) to 1 for internal representation
        value = 1 if value == -1 else (2 if value == 1 else 0)

        bit_index = (row * self.size + col) * 2
        byte_index = bit_index // 8
        bit_offset = bit_index % 8
        
        # Clear the existing 2 bits
        self.board[byte_index] &= ~(3 << bit_offset)
        # Set the new value
        self.board[byte_index] |= (value << bit_offset)

    def get_cell(self, row, col):
        """
        Gets the value at a given (row, col).
        Returns 0 for empty, 1 for white, or -1 for black.
        """
        bit_index = (row * self.size + col) * 2
        byte_index = bit_index // 8
        bit_offset = bit_index % 8
        value = (self.board[byte_index] >> bit_offset) & 3

        # Convert internal representation to -1 for black
        return -1 if value == 1 else (1 if value == 2 else 0)

    def from_2d_array(self, array):
        """
        Converts a 2D array representation (with 0 as empty, 1 as white, and -1 as black)
        into the bitmap representation.
        """
        for row in range(self.size):
            for col in range(self.size):
                self.set_cell(row, col, array[row][col])

    def to_2d_array(self):
        """
        Converts the internal bitmap representation back to a 2D array.
        """
        array = []
        for row in range(self.size):
            row_array = []
            for col in range(self.size):
                row_array.append(self.get_cell(row, col))
            array.append(row_array)
        return array

# Example usage:
board = Board()
input_array = [
    [0, 1, -1, 0, 0, 1, -1, 0],
    [-1, 0, 1, 0, -1, 0, 1, -1],
    [0, -1, 0, 1, 0, -1, 0, 1],
    [1, 0, -1, 0, 1, 0, -1, 0],
    [0, 1, 0, -1, 0, 1, 0, -1],
    [-1, 0, 1, 0, -1, 0, 1, 0],
    [0, -1, 0, 1, 0, -1, 0, 1],
    [1, 0, -1, 0, 1, 0, -1, 0]
]

board.from_2d_array(input_array)
print(board.to_2d_array())


def heuristic(board, turn_color):

    #initial score
    score = 0
    
    # 3 in a row
    # if(check_win == true):
    #     score = +infinity
    if turn_color in check_winner(board):
        #print("got here")
        #print(board)
        return math.inf
    # two in a row - maybe let chains handle this - maybe check for 2 in a row (blocked/unblocked)
    
    # check for chains and increase score using quadratic multiplier
    
    chains, chain_sizes = find_chains(board, turn_color)

    for chain_size in chain_sizes:
        score += chain_size * chain_size
        
    # apply penalty to having adjacent enemies in your chain
    score += penalize_adjacent_enemies_in_chain(board, chains, turn_color)


    #Find distance between chains:
    # chain_centers = []

    # for i in range(chains):
    #     chain_centers[i] = chain_center(i)

    # for i in range(chains-1):
    #     for j in range(i+1, chains):

    tiles = get_tiles(board)


    pulse_weights =[2, 1.5]


    for i in range(len(tiles)):
        #print("Starting ", i)
        #print(tiles[i])
        for j in range(len(pulse_weights)):
            score += get_surrounding_area(board, tiles[i][0], tiles[i][1], pulse_weights[j], pulse_weights[j], j+1)
    
    #find closest peg horizontally, and closest peg vertically

    #make into square, other chain peg is corner, horizontally and vertically  are opposite sides

    #count how many enemy pegs in square, add some 

    return score


def get_tiles(board, turn_color):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    tiles = []
    for i in range(rows):
        for j in range(cols):
            if(board[i][j] == ''):
                tiles.append((i,j))
    return tiles

def get_surrounding_area(board, row, col, fweight, eweight, radius=1):
    """
    Gets the positions surrounding a given cell within a specified radius, applying torus rules (wrapping around edges).

    Parameters:
    grid (list of list): The 2D grid representing the board.
    row (int): Row index of the cell to check.
    col (int): Column index of the cell to check.
    radius (int): Radius to check around the cell.

    Returns:
    list of tuples: List of (row, col) positions within the radius.
    """
    max_row = len(board)
    max_col = len(board[0]) if max_row > 0 else 0

    score = 0
    for r in range(row - radius, row + radius + 1):
        for c in range(col - radius, col + radius + 1):
            # Apply torus wrapping for rows and columns
            wrapped_r = r % max_row
            wrapped_c = c % max_col

            # Check if the position is not the center position
            if (wrapped_r != row or wrapped_c != col):
                if(board[wrapped_r][wrapped_c] == 'B'):
                    score += fweight
                    #print("Near friend at radius: ", radius)
                elif(board[wrapped_r][wrapped_c] != '.'):
                    score -= eweight
                    #print("Near enemy at radius: ", radius)

    return score


# function returns chains with positions as well as list of chain sizes
def find_chains(board, turn_color):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    chains = []

    # Directions: up, down, left, right, and the four diagonals
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def dfs(r, c, chain):
        if visited[r][c]:
            return
        visited[r][c] = True
        if board[r][c] != turn_color:
            return
        chain.append((r, c))
        for dr, dc in directions:
            nr = (r + dr) % rows
            nc = (c + dc) % cols
            if not visited[nr][nc]:
                dfs(nr, nc, chain)

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and board[r][c] == turn_color:
                chain = []
                dfs(r, c, chain)
                if chain:
                    chains.append(chain)

    # Get sizes of all chains
    chain_sizes = [len(chain) for chain in chains]

    return chains, chain_sizes

def penalize_adjacent_enemies_in_chain(board, chains, turn_color):
    score = 0
    board_size = len(board)

    for chain in chains:
        for row, col in chain:
            enemy_color = 'B' if turn_color == 'W' else 'W'

            if board[(row - 1) % board_size][col % board_size] == enemy_color:
                score -= 1
            if board[(row + 1) % board_size][col % board_size] == enemy_color:
                score -= 1
            if board[row % board_size][(col - 1) % board_size] == enemy_color:
                score -= 1
            if board[row % board_size][(col + 1) % board_size] == enemy_color:
                score -= 1
            if board[(row - 1) % board_size][(col - 1) % board_size] == enemy_color:
                score -= 1
            if board[(row + 1) % board_size][(col + 1) % board_size] == enemy_color:
                score -= 1
            if board[(row + 1) % board_size][(col - 1) % board_size] == enemy_color:
                score -= 1
            if board[(row - 1) % board_size][(col + 1) % board_size] == enemy_color:
                score -= 1

    return score


# Example usage:
if __name__ == "__main__":
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
    print(heuristic(board, 'B'))