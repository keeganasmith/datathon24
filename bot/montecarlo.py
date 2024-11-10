import copy
import random
import math
from collections import defaultdict
from common import *
from Board import Board

class Node:
    def __init__(self, board, turn_color, pieces_on_board_dict, maximize_color, moves = None, parent=None):
        self.board = board # state
        self.turn_color = turn_color # state
        self.pieces_on_board_dict = pieces_on_board_dict # state
        self.maximize_color = maximize_color
        self.untried_moves = get_valid_moves(self.board, self.turn_color, self.pieces_on_board_dict[self.turn_color])
        self.parent = parent
        self.move_children = []
        self.children = [] # list of Nodes()
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        # Assumes that each node knows how many moves are possible from the current state
        return len(self.untried_moves) == 0
    
    def best_child(self, exploration_weight=1.41):
        # Selects the child with the highest UCT value
        return max(
            self.children,
            key=lambda child: (child.wins / child.visits) + exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
        )

    def expand(self):
        index = random.randint(0, len(self.untried_moves)-1)
        temp_board = copy.deepcopy(self.board)
        next_turn_color = BLACK
        if(self.turn_color == BLACK):
            next_turn_color = WHITE
        make_move(temp_board, self.untried_moves[index], self.turn_color)

        next_pieces_on_board_dict = copy.deepcopy(self.pieces_on_board_dict)
        if(self.pieces_on_board_dict[self.turn_color] < 8):
            next_pieces_on_board_dict[self.turn_color] += 1
        new_child = Node(temp_board, next_turn_color, next_pieces_on_board_dict,self.maximize_color, parent = self)
        self.children.append(new_child)
        self.move_children.append(self.untried_moves[index])
        del self.untried_moves[index]

        return self.children[-1]
    def is_leaf(self):
        if(len(self.children) == 0):
            return True
        if(self.visits == 0):
            return True
        my_pieces = retrieve_pieces_dictionary(self.board)
        winners = check_winner_efficient(self.board, my_pieces[WHITE], my_pieces[BLACK])
        if(len(winners) != 0):
            return True
        return False
    def is_terminal(self):
        my_pieces = retrieve_pieces_dictionary(self.board)
        winners = check_winner_efficient(self.board, my_pieces[WHITE], my_pieces[BLACK])
        if(len(winners) != 0):
            return True
        return False
    


def monte_carlo_tree_search(root, simulations=1000):
    for _ in range(simulations):
        print("got here")
        node = root
        # Selection
        while not node.is_leaf():
            node = node.best_child()

        # Expansion
        if not node.is_terminal():
            node = node.expand()

        # Simulation
        result = simulate(node)

        # Backpropagation
        backpropagate(node, result)

    # After all simulations, choose the move with the highest visit count
    maximum = -math.inf
    index = 0
    for i in range(0, len(root.children)):
        if root.children[i].visits > maximum:
            maximum = root.children[i].visits
            index = i
    return root.move_children[index]
def winners(board, turn_color):
    my_pieces = retrieve_pieces_dictionary(board)
    winners = check_winner_efficient(board, my_pieces[WHITE], my_pieces[BLACK])
    if turn_color in winners:
        return [turn_color]
    return winners
def simulate(node):
    board = copy.deepcopy(node.board)
    maximize_color = node.maximize_color
    turn_color = node.turn_color
    my_winners = winners(board, turn_color)
    while(len(my_winners)== 0):
        valid_moves = get_valid_moves(board, turn_color, get_piece_count_dict(board)[turn_color])
        index = random.randint(0, len(valid_moves)-1)
        my_move = valid_moves[index]
        make_move(board, my_move, turn_color)
        next_turn_color = BLACK
        if(turn_color == BLACK):
            next_turn_color = WHITE
        turn_color = next_turn_color
        my_winners = winners(board, turn_color)
    return my_winners[0]
def backpropagate(node, winning_color):
    while node is not None:
        node.visits += 1
        if(winning_color == node.turn_color):
            node.wins += 1
        node = node.parent