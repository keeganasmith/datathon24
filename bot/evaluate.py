from common import *
import math
# board is a 8x8 2d array containing pieces that are either W, B, .
# turn_color is W or B
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


def get_tiles(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    tiles = []
    for i in range(rows):
        for j in range(cols):
            if(board[i][j] == 'B'):
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