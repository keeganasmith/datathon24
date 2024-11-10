import copy
import math
import random
from common import *

class GameState:
    def __init__(self, board, turn_color):
        self.board = board
        self.turn_color = turn_color
               
    def get_valid_moves(self):
        return get_valid_moves(self.board, self.turn_color, get_piece_count_dict(self.board)[self.turn_color])

    def apply_move(self, move):
        # Applies a move to the game state and switches to the next player
        new_board = copy.deepcopy(self.board)
        make_move(new_board, move, self.turn_color)
        self.turn_color = -self.turn_color
        return GameState(new_board, self.turn_color) # THIS might need to be deep copies here probably

    def is_terminal(self):
        # Checks if the game has reached a win, loss, or draw state
        pieces = retrieve_pieces_dictionary(self.board)
        if check_winner_for_color(self.board, pieces[self.turn_color], self.turn_color):
            return True
        if check_winner_for_color(self.board, pieces[-self.turn_color], -self.turn_color):
            return True
        return False

    def get_winner(self):
        # Returns the winner if there is one, or None otherwise
        pieces = retrieve_pieces_dictionary(self.board)
        winners = check_winner_efficient(self.board, pieces[WHITE], pieces[BLACK])
        if(len(winners) > 1):
            return -self.turn_color
        
        if len(winners) > 0:
            return winners[0]
        return None
    

class Node:
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = game_state.get_valid_moves()
        self.children_moves = []

    def is_fully_expanded(self):
        # print(self.untried_moves)
        return len(self.untried_moves) == 0

    def best_child(self, exploration_weight=50):
        # print(self.parent)
        # print(self.game_state.board.board)
        return max(
            self.children,
            key=lambda child: (child.wins / child.visits) +
                              exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
        )

    def expand(self):
        move = self.untried_moves.pop()
        next_state = self.game_state.apply_move(move)
        child_node = Node(next_state, parent=self)
        self.children.append(child_node)
        self.children_moves.append(move)
        return child_node

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)




def monte_carlo_tree_search(root, simulations=1000):
    for _ in range(simulations):
        # Selection
        node = root
        while node.is_fully_expanded() and not node.game_state.is_terminal():
            # print(node.children)
            # if node.children == []:
            #     break
            node = node.best_child()

        # Expansion
        if not node.game_state.is_terminal():
            node = node.expand()

        # Simulation
        result = simulate(node)

        # Backpropagation
        node.backpropagate(result)

    # Choose the most visited child as the best move
    maxi = -math.inf
    max_index = 0
    for idx, child in enumerate(root.children):
        if child.visits > maxi:
            maxi = child.visits
            max_index = idx
    return root.children_moves[max_index]

def simulate(node):
    state = node.game_state
    while not state.is_terminal():
        move = random.choice(state.get_valid_moves())
        state = state.apply_move(move)

    # Assume +1 for win, 0 for draw, -1 for loss
    winner = state.get_winner()
    if winner == node.game_state.turn_color:
        return 1
    elif winner is None:
        return 0
    else:
        return -1
