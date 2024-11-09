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
    
    #check for chains and increase score using quadratic multiplier
    
    chains, chain_sizes = find_chains(board, turn_color)
    for chain_size in chain_sizes:
        score += chain_size * chain_size

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

# Example usage:
if __name__ == "__main__":
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
    print(evaluate_board(board, 'B'))