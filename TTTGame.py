from copy import deepcopy
import numpy as np  # use numpy arays much easier to find diagonal objects

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
        


    def generate_children(self):
        # recursively generates children 

        ''' function subject to change not too sure wether to generate the entire game upon start up and then use specifc values for performance reasons
            generating every time opponent moves could be long however cba implementing it '''

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
        # find row of 3 inside the board state used to stop reccursive generation of children
        # so that impposible board states aren't created
        for row in self.state:
            if all(x == row[0] for x in row) and row[0] is not None:
                return True
            
        for column in self.state.transpose():
            if all(x == column[0] for x in column) and column[0] is not None:
                return True
        
        if all(x == self.state.diagonal()[0] for x in self.state.diagonal()) and self.state.diagonal()[0] is not None: # diagonal
            return True

        elif all(x == np.fliplr(self.state).diagonal()[0] for x in np.fliplr(self.state).diagonal()) and np.fliplr(self.state).diagonal()[0] is not None:  # flip list horizontally
            return True

        elif all(x == np.fliplr(self.state).diagonal()[0] for x in np.flipud(self.state).diagonal()) and np.flipud(self.state).diagonal()[0] is not None:  # flip vertically
            return True
        
        elif all(x == np.flipud(np.fliplr(self.state)).diagonal()[0] for x in np.flipud(np.fliplr(self.state).diagonal())) and np.flipud(np.fliplr(self.state)).diagonal()[0] is not None:  # flip horizontally and vertically
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


board = Board(start, 0, 'O')

tree = {}
def populate_tree(item, n):
    tree[item] = []
    for i in item.generate_children():
        if n > 0:
            tree[item].append(i.state)
            populate_tree(i, n-1)
    return tree
populate_tree(board, 1)
print(tree)
