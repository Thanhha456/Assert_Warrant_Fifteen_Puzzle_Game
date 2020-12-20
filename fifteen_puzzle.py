"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

# import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if target_row >= 0:
            if self._grid[target_row][target_col] == 0:
                if target_row == self._height - 1:
                    if target_col == self._width-1:
                        return True
                    else:
                        for dummy_col in range(self._width):
                            if self._grid[self._height - 1][dummy_col] == dummy_col + self._width * (self._height - 1):
                                    return True
                else:
                    if target_col == self._width-1:
                        for dummy_row in range(target_row + 1, self._height):
                            for dummy_col in range(self._width):
                                if self._grid[target_row + 1][dummy_col] == dummy_col + self._width * (target_row + 1):
                                    return True
                                return False
                    else:
                        for dummy_idx in range(target_col + 1, self._width):
                            if self._grid[target_row][dummy_idx] == dummy_idx + self._width * target_row:
                                for dummy_row in range(target_row + 1, self._height):
                                    for dummy_col in range(self._width):                                      
                                        if self._grid[dummy_row][dummy_col] == dummy_col + self._width * dummy_row:
                                            return True
                                        return False
                            return False
        return False


    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        current_pos = self.current_position(target_row, target_col)
        target_pos = target_row, target_col        
        assert self.lower_row_invariant(target_row, target_col)
        move_string = self.position_tile(current_pos, target_pos)
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col - 1)

        return move_string

    def position_tile(self, current_pos, target_pos):
        """
         Helper function that positions a target_tile to (target_row, target_col)
        and returns the move_string that will get it there
        :param current_pos:
        :param target_pos:
        :return:
        """
        move_string = ""
        if target_pos[1] >= 0:
            if current_pos[0] == target_pos[0]:
                if current_pos[1] <= target_pos[1]:
                    for dummy in range(target_pos[1] - current_pos[1]):
                        move_string += "l"
                    for dummy in range(target_pos[1] - current_pos[1] - 1):
                        move_string += "urrdl"

            if current_pos[0] < target_pos[0]:
                for dummy in range(target_pos[0] - current_pos[0]):
                    move_string += "u"
                if current_pos[1] == target_pos[1]:
                    for dummy in range(target_pos[0] - current_pos[0] - 1):
                        move_string += "lddru"
                    move_string += "ld"

                elif current_pos[1] < target_pos[1] :
                    for dummy in range(target_pos[1] - current_pos[1]):
                        move_string += "l"
                    for dummy in range(target_pos[1] - current_pos[1] - 1):
                            move_string += "drrul"
                    move_string += "dru"
                    for dummy in range( target_pos[0] - current_pos[0] - 1):
                        move_string += "lddru"
                    move_string += "ld"

                elif current_pos[1] > target_pos[1]:
                    for dummy in range(current_pos[1] - target_pos[1]):
                        move_string += "r"
                    for dummy in range(current_pos[1] - target_pos[1] - 1):
                        if current_pos[0] == 0:
                            move_string += "dllur"
                        else:
                            move_string += "ulldr"
                    if current_pos[0] == 0:
                        if target_pos[0] - current_pos[0] == 1:
                            move_string += "dlu"
                        else :
                            move_string += "dlulddru"
                    else:
                        move_string += "ullddru"
                    for dummy in range( target_pos[0] - current_pos[0] - 2):
                        move_string += "lddru"
                    move_string += "ld"
        return move_string


    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        current_pos = self.current_position(target_row, 0)
        assert self.lower_row_invariant(target_row, 0) == True
        move_string = "ur"
        if current_pos[0] == target_row -1:
            for dummy in range(self._width - 2):
                move_string += "r"
        else:
            if target_row >= 1:
                target_pos = target_row - 1, 1
                move_string += self.position_tile(current_pos, target_pos)
                move_string += "ruldrdlurdluurddlur"
                for dummy in range(self._width - 2):
                    move_string += "r"
        self.update_puzzle(move_string)
     #   assert self.lower_row_invariant(target_row - 1, self._width - 1) == True

        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if target_col >= 0:
            if self._grid[0][target_col] == 0:
                if target_col == self._width:
                    if self.lower_row_invariant(0, target_col) ==  True :
                        return True
                    else:
                        return False
                else:
                    for dummy in range(target_col +1,self._width):
                        if self._grid[0][dummy] == dummy:
                            if self._grid[1][target_col] == target_col + self._width:
                                return True
                            return False
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        if target_col >= 0:
            if self._grid[1][target_col] == 0:
                if self.lower_row_invariant(1, target_col) ==  True :
                    return True
                return False

        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        move_string = ""
        current_pos = self.current_position(0, target_col)
        if self._grid[0][target_col] == target_col:
            return ""
        elif current_pos[0] == 0 and current_pos[1] == target_col - 1:
            move_string += "ld"
            self.update_puzzle(move_string)
            return move_string
        else:
            if current_pos[0] == 0 and current_pos[1] == target_col - 2:
                move_string += "ll"
                move_string += "druld"
            elif current_pos[0] == 1 and current_pos[1] == target_col - 2:
                move_string += "ldl"   
            elif current_pos[0] == 0:
                for dummy_0 in range(target_col - current_pos[1]):
                    move_string += "l"
                for dummy_x  in range(target_col - current_pos[1] - 2):
                    move_string += "drrul"
                move_string += "druld"
                
            elif current_pos[0] == 1:
                move_string += "ld"
                for dummy_0 in range(target_col - current_pos[1] - 1):
                    move_string += "l"
                for dummy_x in range(target_col - current_pos[1] - 2):
                    move_string += "urrdl"
        move_string += "urdlurrdluldrruld"
        self.update_puzzle(move_string)
        assert self.row1_invariant(target_col - 1)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        move_string = ""
        current_pos = self.current_position(1, target_col)
        if self._grid[1][target_col] == target_col + self._width:
            move_string = ""
        elif current_pos[0] == 1:
            for dummy in range(target_col - current_pos[1]):
                move_string += "l"
            for dummy_1 in range(target_col - current_pos[1] - 1):
                move_string += "urrdlur"
                self.update_puzzle(move_string)
                return move_string
        elif current_pos[0] == 0:
            move_string += "u"
            if target_col == current_pos[1]:
                move_string += "ld"
            elif target_col > current_pos[1]:
                for dummy in range(target_col - current_pos[1]):
                    move_string += "l"
                if target_col == current_pos[1] + 1:
                        move_string += "druld"
                elif target_col > current_pos[1] - 2:
                    for dummy in range(target_col - current_pos[1] - 1):
                        move_string += "drrul"
                    move_string += "druld"

            else:
                target_pos = 0, target_col
                move_string += self.position_tile(current_pos, target_pos)
                move_string += "d"
        move_string += "ur"
        self.update_puzzle(move_string)
     #   assert self.row1_invariant( target_col-1)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        move_string = ""
        assert self.lower_row_invariant(1, 1)
        if self._grid[0][0] == 1 and self._grid[1][0] == self._width:
            move_string += "ul"
        elif self._grid[1][0] == self._width and self._grid[0][1] == 1:
            move_string += "lur"
        elif self._grid[1][0] == self._width + 1 and self._grid[0][1] == 1:
            move_string += "lu"
        else:
            move_string += "uldrul"
        self.update_puzzle(move_string)
        if self._grid[0][1] == 1 and self._grid[1][0] == self._width:
            
            return move_string
        else:
            return "0"
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_string0 = ""
        _idxy = self._width - 1
        _idxx = self._height-1
        zero_pos = 0, 0
            
        #find the zero position
        for dummy_x in range(self._height):
            for dummy_y in range(self._width):
                if self._grid[dummy_x][dummy_y] == 0:
                    zero_pos = dummy_x, dummy_y
        # find the target position            
        if self._grid[self._height-1][self._width - 1] != 0:
            while _idxx > 1:
                if self._grid[_idxx][_idxy] == _idxy + self._width * _idxx:
                    _idxy -= 1
                else:
                    break
                if _idxy < 0:
                    _idxy = self._width - 1
                    _idxx -= 1
        if self._grid[self._height-1][self._width -1] == 0:
            _idxx, _idxy = self._height-1, self._width - 1
            
        # move the zero to the target position       
        if zero_pos[1] <= _idxy:
            for dummy in range(_idxy - zero_pos[1]):
                 move_string0 += "r"
        if zero_pos[1] > _idxy:
            for dummy in range(zero_pos[1]-_idxy):
                move_string0 += "l"
        for dummy in range(_idxx - zero_pos[0]): 
            move_string0 += "d"
        self.update_puzzle(move_string0)
        move_string = ""
        while True and _idxx > 1:
            move_string += self.solve_interior_tile(_idxx, _idxy)
            _idxy -= 1
            if _idxy == 0:
                move_string += self.solve_col0_tile(_idxx)
                _idxy = self._width - 1
                _idxx -= 1
                print(self._grid)
        if _idxx == 1:
            while _idxy > 1:
                assert self.row1_invariant(_idxy)
                move_string += self.solve_row1_tile(_idxy)
#                assert self.row1_invariant(_idxy -1)
                move_string += self.solve_row0_tile(_idxy)
                assert self.row1_invariant(_idxy-1)
                _idxy -= 1
          
            if _idxy == 1 :
                assert self.row1_invariant(1)
                move_string += self.solve_2x2()
                

            if _idxy == 0  : 
                if self._grid[0][0] == self._width:
                    move_string += "u"
                elif self._grid[0][0] == 0:
                    self.update_puzzle(move_string)
        move_string = move_string0 + move_string
        
        return move_string


# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
#obj = Puzzle(4, 5, [[1, 2, 0, 3, 4], [6, 5, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.solve_row0_tile(2) 
# obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
# print(obj.solve_puzzle())
#obj = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#print obj.solve_puzzle()
#obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print obj.solve_row0_tile(2) 
#obj = Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.solve_row0_tile(4)
#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print obj.row0_invariant(2) 