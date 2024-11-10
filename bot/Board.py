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
    def to_string(self):
        result = ""
        for row in range(self.size):
            for col in range(self.size):
                result += str(self.get_cell(row, col))
        return result