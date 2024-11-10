import copy
import random
import math
from collections import defaultdict
from common import *


class Node:
    def __init__(self, board, turn_color, pieces_on_board_dict, moves, parent=None):
        self.board = board # state
        self.turn_color = turn_color # state
        self.pieces_on_board_dict = pieces_on_board_dict # state
        self.moves = moves # state
        self.parent = parent
        self.children = [] # list of Nodes()
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        # Assumes that each node knows how many moves are possible from the current state
        return len(self.children) == len(get_valid_moves(self.board, self.turn_color, self.pieces_on_board_dict[self.turn_color]))
    
    def best_child(self, exploration_weight=1.41):
        # Selects the child with the highest UCT value
        return max(
            self.children,
            key=lambda child: (child.wins / child.visits) + exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
        )

    def expand(self):
        # Expands the tree by creating a child node for each possible move not yet explored
        
        # Get all possible moves from the current state
        possible_moves = get_valid_moves(self.board, self.turn_color, self.pieces_on_board_dict[self.turn_color])

        children_boards = []
        for move in possible_moves:
            temp_board = copy.deepcopy(self.board)
            make_move(temp_board, move, self.turn_color)
            children_boards.append(temp_board)
           
        tried_boards = [] 
        for child in self.children:
            tried_boards.append(child.board)

        # Filter out the moves that have already been tried
        untried_boards = []
        for move in possible_moves:
            temp_board = copy.deepcopy(self.board)
            make_move(temp_board, move, self.turn_color)
            if temp_board not in tried_boards:
                untried_boards.append(move)
        
        move = random.choice(untried_moves)
        new_state = self.state.apply_move(move)
        child_node = Node(new_state, parent=self)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        # Updates the node's statistics based on the result of a simulation
        self.visits += 1
        self.wins += result


def monte_carlo_tree_search(root, simulations=1000):
    for _ in range(simulations):
        node = root
        # Selection
        while not node.state.is_terminal() and node.is_fully_expanded():
            node = node.best_child()

        # Expansion
        if not node.state.is_terminal():
            node = node.expand()

        # Simulation
        result = simulate(node.state)

        # Backpropagation
        backpropagate(node, result)

    # After all simulations, choose the move with the highest visit count
    return max(root.children, key=lambda child: child.visits).state


def simulate(state):
    current_state = state
    while not current_state.is_terminal():
        possible_moves = current_state.get_possible_moves()
        # Heuristic to prefer moves that lead to potential 3-in-a-row
        move = random.choice(possible_moves)
        current_state = current_state.apply_move(move)
    return current_state.get_result()


def backpropagate(node, result):
    while node is not None:
        node.visits += 1
        # Add wins if the result is favorable for the player at that node
        node.wins += result if node.state.player_turn == 1 else (1 - result)
        node = node.parent


# Initialize the root state for Pop Tac Toe
root_state = PopTacToeState(initial_board, player_turn)
root_node = Node(root_state)

# Run MCTS
best_final_state = monte_carlo_tree_search(root_node, simulations=1000)
