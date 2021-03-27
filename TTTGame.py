from copy import deepcopy
import numpy as np  # use numpy arays much easier to find diagonal objects
from itertools import groupby
import pprint
import time

start_time = time.time()
start = np.array([[None for row in range(3)] for column in range(3)]) # 2d 3x3 array populated with none values


class Board:

    ''' Class to represent the current state of the board 
        
        state - the current layout of the board in this case a 2d array
        score - the current score after evaluation of the board used for minmaxing

    '''
    def __init__(self, state, score, turn, *parent):
        self.state = state  # child_board[row][i] state of the board given as 2d array
        self.score = score  # child_board[row][i] value of the (used for minmaxing later)
        parent = None
        self.turn = turn
        self.children = np.array([]) # later populated by the generate children function

        # create alternate staes of board list. used later when checking for win states and score heuristic
        self.alt_states = []
        self.alt_states.append(self.state.transpose())
        self.alt_states.append(self.diagonal())
        self.alt_states.append(np.fliplr(self.state).diagonal())
        self.alt_states.append(np.flipud(self.state).diagonal())
        self.alt_states.append(np.flipud.fliplr(self.state).daigonal())


    def generate_children(self):
        # recursively generates children 
        # lazy loads children so function later can call it to a given depth
        for row in range(3): 
            for i in range(3):
                child_board = deepcopy(self.state)  # copys list instead of just referencing it because python sucks dick
                # changes a space if none and will change to a naught or a cross depending on whos turn it is
                if child_board[row][i] is None: 
                    child_board[row][i] = self.turn
                    yield Board(child_board, 0, self.change_turn(self.turn)) 

        # recursive  that iterates through all the children just created and generates those related boards
        self.turn = self.change_turn(self.turn)
        for child in self.children:
            if not child.is_win():
                child.generate_children()

    def is_win(self):
        ''' find row of 3 inside the board state used to stop reccursive generation of children
         so that impposible board states aren't created '''
        for row in self.state:
            if all(x == row[0] for x in row) and row[0] is not None:
                return True
            
        for states in self.alt_states:
            if all(x == state[0] for x in state) and state[0] is not None:
                return True
        else:
            return False

    def change_turn(self, turn):
        if turn == 'O':
            turn = 'X'
            return turn
        else:
            turn == 'O'
            return turn

    def evaluate_board(self): 
        # This function is probably really inefficient plans to replace this with some type of numpy alternative
        score = float('-inf')
        for row in self.state:
            grouped_row = [(k, sum(1 for i in g)) for k,g in groupby(row)]
            for item in grouped_row:
                if item[0] == 'X':
                    score += item[1]
        return score 
            
# reccursive function to populate a dictionary with board objects as keys and vlaues are dictionarys of other board items
def populate_tree(item, depth, tree):
    tree[item] = {}
    for i in item.generate_children():
        if depth > 0:
            tree[item][i] = {}
            populate_tree(i, depth-1, tree[item])  # calls the fuction again but uses the parent as the root tree
    return tree


