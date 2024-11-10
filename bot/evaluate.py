from common import *
import math
from Board import Board
# board is a 8x8 2d array containing pieces that are either W, B, .
# turn_color is W or B

def heuristic(board, turn_color, pieces):

    #initial score
    score = 0
    chain_score_weight = .6
    pulse_score_weight = .4
    
    # 3 in a row
    # if(check_win == true):
    #     score = +infinity
    if check_winner_for_color(board, pieces, turn_color):
        return math.inf
    
    # Chain Heuristic - (i.e 2 in a row) - maybe add a bonus for 2 in a row being unblocked on both sides? or is pulse handling this?
    chains, chain_sizes = find_chains(board, turn_color)
    chain_score = 0
    for chain_size in chain_sizes:
        if chain_size > 1:
            chain_score += chain_size
    chain_score /= 8

    # Pulse Heuristic
    pulse_weights =[2, 1.5]
    pulse_score = 0
    
    for i in range(len(pieces)):
        for j in range(len(pulse_weights)):
            pulse_score += get_surrounding_area(board, pieces[i][0], pieces[i][1], pulse_weights[j], turn_color, j+1)

    pulse_score /= 40
    score += chain_score * chain_score_weight + pulse_score * pulse_score_weight

    return score

def get_surrounding_area(board, row, col, fweight, turn_color, radius=1):
    max_row = 8
    max_col = 8

    score = 0
    for r in range(row - radius, row + radius + 1):
        for c in range(col - radius, col + radius + 1):
            # Apply torus wrapping for rows and columns
            wrapped_r = r % max_row
            wrapped_c = c % max_col

            # Check if the position is not the center position
            if (wrapped_r != row or wrapped_c != col):
                if(board.get_cell(wrapped_r, wrapped_c) == turn_color):
                    score += fweight
                    #print("Near friend at radius: ", radius)
                    #print("Near enemy at radius: ", radius)

    return score


# function returns chains with positions as well as list of chain sizes
def find_chains(board, turn_color):
    rows = 8
    cols = 8
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    chains = []

    # Directions: up, down, left, right, and the four diagonals
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def dfs(r, c, chain):
        if visited[r][c]:
            return
        visited[r][c] = True
        if board.get_cell(r,c) != turn_color:
            return
        chain.append((r, c))
        for dr, dc in directions:
            nr = (r + dr) % rows
            nc = (c + dc) % cols
            if not visited[nr][nc]:
                dfs(nr, nc, chain)

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and board.get_cell(r,c) == turn_color:
                chain = []
                dfs(r, c, chain)
                if chain:
                    chains.append(chain)

    # Get sizes of all chains
    chain_sizes = [len(chain) for chain in chains]

    return chains, chain_sizes