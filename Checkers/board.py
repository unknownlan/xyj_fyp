from .piece import Piece
from .constants import *
from copy import deepcopy, copy
import gym
import numpy as np

class Board:
    def __init__(self):
        self.board = []
        self.selected = 0
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()

    @staticmethod
    def draw_squares(win):
        win.fill(BLACK)
        for row in range(ROWS):
            if row % 2 == 0:
                for col in range(ROWS):
                    if col % 2 == 0:
                        win.blit(texture03, (SQUARE_SIZE * col, SQUARE_SIZE * row))
                    else:
                        win.blit(texture04, (SQUARE_SIZE * col, SQUARE_SIZE * row))
            else:
                for col in range(ROWS):
                    if col % 2 != 0:
                        win.blit(texture03, (SQUARE_SIZE * col, SQUARE_SIZE * row))
                    else:
                        win.blit(texture04, (SQUARE_SIZE * col, SQUARE_SIZE * row))
## start of code i wrote
    def create_board(self):
        """init board"""
        self.board = []
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw_piece(win)

    def move(self, piece, row, col):
        """move checker"""
        if not piece:
            return False

        # original position
        old_row, old_col = piece.row, piece.col
        
        # change position
        self.board[old_row][old_col], self.board[row][col] = self.board[row][col], self.board[old_row][old_col]
        
        # update 
        piece.move(row, col)
        
        # to king
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1
            
        return True
## end of code i wrote
    def get_piece(self, row, col):
        return self.board[row][col]
## start of code i wrote
    def print_board_state(self):
        """get board state"""
        print("\nCurrent Board State:")
        for row in range(ROWS):
            row_str = ""
            for col in range(COLS):
                piece = self.board[row][col]
                if piece == 0:
                    row_str += "[ ]"
                elif piece.color == WHITE:
                    row_str += "[W]" if not piece.king else "[WK]"
                else:
                    row_str += "[B]" if not piece.king else "[BK]"
            print(row_str)
        print()

    def get_valid_moves(self, piece):
        """get all valid move"""
        if not piece:
            return {}

        print(f"\nChecking moves for piece at ({piece.row}, {piece.col}) color: {'WHITE' if piece.color == WHITE else 'BLACK'}")
        
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # check jumpeat and normal move
        if piece.color == BLACK:  # black move up
            print("Checking BLACK piece moves")
            # normal move
            if row - 1 >= 0:
                # left move
                if left >= 0:
                    if self.board[row - 1][left] == 0:  # normal move
                        moves[(row - 1, left)] = []
                        print(f"Found valid move to ({row - 1}, {left})")
                    # jump eat move
                    elif (self.board[row - 1][left] != 0 and 
                          self.board[row - 1][left].color == WHITE and 
                          row - 2 >= 0 and left - 1 >= 0 and 
                          self.board[row - 2][left - 1] == 0):
                        moves[(row - 2, left - 1)] = [self.board[row - 1][left]]
                        print(f"Found jump move to ({row - 2}, {left - 1})")

                # right up move
                if right < COLS:
                    if self.board[row - 1][right] == 0:  # normal move
                        moves[(row - 1, right)] = []
                        print(f"Found valid move to ({row - 1}, {right})")
                    # jump eat 
                    elif (self.board[row - 1][right] != 0 and 
                          self.board[row - 1][right].color == WHITE and 
                          row - 2 >= 0 and right + 1 < COLS and 
                          self.board[row - 2][right + 1] == 0):
                        moves[(row - 2, right + 1)] = [self.board[row - 1][right]]
                        print(f"Found jump move to ({row - 2}, {right + 1})")

        if piece.color == WHITE:  # white downwards
            print("Checking WHITE piece moves")
            # normal move
            if row + 1 < ROWS:
                # left downward 
                if left >= 0:
                    if self.board[row + 1][left] == 0:  # normal move 
                        moves[(row + 1, left)] = []
                        print(f"Found valid move to ({row + 1}, {left})")
                    # jump eat move
                    elif (self.board[row + 1][left] != 0 and 
                          self.board[row + 1][left].color == BLACK and 
                          row + 2 < ROWS and left - 1 >= 0 and 
                          self.board[row + 2][left - 1] == 0):
                        moves[(row + 2, left - 1)] = [self.board[row + 1][left]]
                        print(f"Found jump move to ({row + 2}, {left - 1})")

                # right downward move
                if right < COLS:
                    if self.board[row + 1][right] == 0:  # normal move 
                        moves[(row + 1, right)] = []
                        print(f"Found valid move to ({row + 1}, {right})")
                    # jump eat move
                    elif (self.board[row + 1][right] != 0 and 
                          self.board[row + 1][right].color == BLACK and 
                          row + 2 < ROWS and right + 1 < COLS and 
                          self.board[row + 2][right + 1] == 0):
                        moves[(row + 2, right + 1)] = [self.board[row + 1][right]]
                        print(f"Found jump move to ({row + 2}, {right + 1})")

        # If it's a king, add a reverse move
        if piece.king:
            king_moves = {}
            if piece.color == BLACK:  # The Black King moves down.
                if row + 1 < ROWS:
                    if left >= 0 and self.board[row + 1][left] == 0:
                        king_moves[(row + 1, left)] = []
                    if right < COLS and self.board[row + 1][right] == 0:
                        king_moves[(row + 1, right)] = []

            if piece.color == WHITE:  # The white King moves down.
                if row - 1 >= 0:
                    if left >= 0 and self.board[row - 1][left] == 0:
                        king_moves[(row - 1, left)] = []
                    if right < COLS and self.board[row - 1][right] == 0:
                        king_moves[(row - 1, right)] = []

            moves.update(king_moves)

        # If there is a jump-eat move, only the jump-eat move is returned
        jumps = {move: skip for move, skip in moves.items() if skip}
        if jumps:
            print(f"Found jump moves: {jumps}")
            return jumps

        print(f"Found regular moves: {moves}")
        return moves

    def remove(self, pieces):
        for piece in pieces:
            print(f"Removing piece at ({piece.row}, {piece.col}) with color {piece.color}")  # debug
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                elif piece.color == WHITE:
                    self.white_left -= 1

    def winner(self):
        if self.white_left == 0:
            return BLACK
        elif self.black_left == 0:
            return WHITE
        else:
            return None

    def evaluate(self):
        # evaluate
        return (
            self.white_left - self.black_left + 
            (self.white_kings * 1.5 - self.black_kings * 1.5) +  # king weight higher
            self._evaluate_position() +  # piece position
            self._evaluate_mobility()    # mobility
        )

    def _evaluate_position(self):
        # Evaluating Positional Advantages of Pieces
        score = 0
        for piece in self.get_all_pieces(WHITE):
            score += (7 - piece.row) * 0.1  # closer get to the other team's bottom line, the higher score.
        for piece in self.get_all_pieces(BLACK): 
            score -= piece.row * 0.1
        return score

    def _evaluate_mobility(self):
        # evaluate mobility
        white_moves = sum(len(self.get_valid_moves(p)) for p in self.get_all_pieces(WHITE))
        black_moves = sum(len(self.get_valid_moves(p)) for p in self.get_all_pieces(BLACK))
        return (white_moves - black_moves) * 0.05

    def get_all_pieces(self, color):
        """get all pieces"""
        pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def __str__(self):
        """print state"""
        board_str = ""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece == 0:
                    board_str += "[ ]"
                elif piece.color == WHITE:
                    board_str += "[■]" if not piece.king else "[♔]"
                else:
                    board_str += "[●]" if not piece.king else "[♚]"
            board_str += "\n"
        return board_str

    def copy_board(self):
        board = []
        for r, row in enumerate(self.board):
            board.append([])
            for piece in row:
                if piece != 0:
                    board[r].append(piece.copy())
                else:
                    board[r].append(piece)
        return board

    def copy(self):
        copyobj = Board()
        for name, attr in self.__dict__.items():
            if name == 'board':
                board = self.copy_board()
                setattr(copyobj, 'board', board)
            elif hasattr(attr, 'copy') and callable(getattr(attr, 'copy')) and name != 'board':
                copyobj.__dict__[name] = copy(attr)
            else:
                copyobj.__dict__[name] = deepcopy(attr)
        return copyobj
    
    def get_state(self):
        """Convert the board state to an 8x8 matrix."""
        state = []
        for row in self.board:
            state_row = []
            for cell in row:
                if isinstance(cell, Piece):
                    state_row.append(1 if cell.color == WHITE else -1)
                else:
                    state_row.append(0)
            state.append(state_row)
        return np.array(state, dtype=np.int8)

## end of code i wrote