## start of code i wrote
from .board import *
from .piece import *
from .constants import *
from Checkers.abel_algo import AbelPPOAI  
from Checkers.kane_algo import *  
from CheckersEnv import CheckersEnv

class Game:
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK  # black first
        self.valid_moves = {}
        self.board.create_board()  # Make sure the board is properly initialised

    def __init__(self, win, white_type="Human", black_type="Human"):
        self._init()
        self.win = win
        self.white_type = white_type
        self.black_type = black_type
        self.white_ai = None
        self.black_ai = None

        # init AI
        try:
            if white_type == "Abel":
                self.white_ai = AbelPPOAI(model_path="models/abel_final_model")
                print("White Abel AI initialized")
            if black_type == "Abel":
                self.black_ai = AbelPPOAI(model_path="models/abel_final_model")
                print("Black Abel AI initialized")
        except Exception as e:
            print(f"Error initializing AI: {e}")

    def get_board(self):
        return self.board

    def reset(self):
        self._init()

    def update(self):
        self.board.draw(self.win)
        if self.selected and self.selected.color == self.turn:
            self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row, col):
        """Logic to handle selection and movement of pieces"""
        # If it's not a human player's turn, return directly
        if ((self.turn == WHITE and self.white_type != "Human") or 
            (self.turn == BLACK and self.black_type != "Human")):
            return False

        # If a piece is already selected
        if self.selected:
            # Trying to move to a new location
            result = self._move(row, col)
            if not result:
                # If the move fails, check to see if a new piece for your side has been selected.
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == self.turn:
                    # Check for forced food skipping
                    has_jumps = self._check_forced_jumps()
                    if has_jumps:
                        valid_moves = self.board.get_valid_moves(piece)
                        if any(skip for _, skip in valid_moves.items()):
                            self.selected = piece
                            self.valid_moves = valid_moves
                            return True
                    else:
                        self.selected = piece
                        self.valid_moves = self.board.get_valid_moves(piece)
                        return True
                # If you can neither move nor select a new piece, cancel the selection.
                self.selected = None
                self.valid_moves = {}
            return result

        # If no piece is selected yet
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            # Check for forced food skipping
            has_jumps = self._check_forced_jumps()
            if has_jumps:
                valid_moves = self.board.get_valid_moves(piece)
                if any(skip for _, skip in valid_moves.items()):
                    self.selected = piece
                    self.valid_moves = valid_moves
                    return True
            else:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True

        return False

    def _check_forced_jumps(self):
        """Check for forced food skipping"""
        for piece in self.board.get_all_pieces(self.turn):
            valid_moves = self.board.get_valid_moves(piece)
            if any(skip for _, skip in valid_moves.items()):
                return True
        return False

    def _move(self, row, col):
        """move"""
        piece = self.selected
        if not piece or (row, col) not in self.valid_moves:
            return False

        # Save the position before the move
        old_row, old_col = piece.row, piece.col

        # action
        if not self.board.move(piece, row, col):
            return False

        # handle jump eat
        skipped = self.valid_moves.get((row, col))
        if skipped:
            self.board.remove(skipped)
            
            # Check if it's okay to keep jump eats
            next_moves = self.board.get_valid_moves(piece)
            next_jumps = {move: skip for move, skip in next_moves.items() if skip}
            
            if next_jumps:
                self.valid_moves = next_jumps
                self.selected = piece
                return True

        # If you can't continue to jump and eat, switch rounds
        self.change_turn()
        return True

    def change_turn(self):
        """turns"""
        self.valid_moves = {}
        self.selected = None
        self.turn = WHITE if self.turn == BLACK else BLACK

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win, BLUE,
                (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 8
            )

    def winner(self):
        """winner check"""
        # check pieces
        white_pieces = self.board.get_all_pieces(WHITE)
        black_pieces = self.board.get_all_pieces(BLACK)
        
        # If one side has no discs, the other side wins.
        if not white_pieces:
            print("Black wins - White has no pieces")
            return BLACK
        if not black_pieces:
            print("White wins - Black has no pieces")
            return WHITE
        
        # Checks if the current player has a legal move
        if not self.check_valid_moves():
            winner_color = WHITE if self.turn == BLACK else BLACK
            print(f"{'White' if winner_color == WHITE else 'Black'} wins - Current player has no valid moves")
            return winner_color
        
        return None

    def check_game_over(self):
        """check game over"""
        # check winner
        winner = self.board.winner()
        if winner is not None:
            print(f"Game over! Winner: {winner}")
            return True

        # Get all the current player's pieces and possible moves
        valid_moves_exist = False
        for piece in self.board.get_all_pieces(self.turn):
            moves = self.board.get_valid_moves(piece)
            if moves:
                valid_moves_exist = True
                break

        if not valid_moves_exist:
            print(f"Game over! {self.turn} has no valid moves")
            return True

        return False

    def get_valid_moves(self, piece):
        """get valid move"""
        if not piece:
            return {}
        
        # Make sure the colour of the pieces matches the current turn
        if piece.color != self.turn:
            return {}
        
        moves = self.board.get_valid_moves(piece)
        
        # If there is a skip-eat move, the skip-eat must be performed
        jumps = {move: skip for move, skip in moves.items() if skip}
        if jumps:
            return jumps
        return moves

    def check_valid_moves(self):
        """check valid move"""
        print(f"\nChecking valid moves for {'WHITE' if self.turn == WHITE else 'BLACK'} player")
        self.board.print_board_state()
        
        pieces = self.board.get_all_pieces(self.turn)
        print(f"Found {len(pieces)} pieces")
        
        for piece in pieces:
            moves = self.board.get_valid_moves(piece)
            if moves:
                print(f"Found valid moves for piece at ({piece.row}, {piece.col}): {moves}")
                return True
        print("No valid moves found")
        return False

    def ai_move(self):
        """handle ai"""
        if not self.check_valid_moves():
            print(f"No valid moves for {self.turn}")
            self.change_turn()
            return False

        # ai move
        if self.turn == WHITE:
            if self.white_type == "Kane":
                return self.kane_ai_move()
            elif self.white_type == "Abel":
                return self.abel_ai_move(self.white_ai)
        elif self.turn == BLACK:
            if self.black_type == "Kane":
                return self.kane_ai_move()
            elif self.black_type == "Abel":
                return self.abel_ai_move(self.black_ai)
        return False

    def kane_ai_move(self):
        """handle Kane AI move"""
        try:
            print("\nKane AI thinking...")
            # possible move
            all_pieces = self.board.get_all_pieces(self.turn)
            if not all_pieces:
                print("No pieces available")
                return False

            # find all possible move
            all_moves = {}
            for piece in all_pieces:
                valid_moves = self.board.get_valid_moves(piece)
                if valid_moves:
                    all_moves[piece] = valid_moves

            if not all_moves:
                print("No valid moves available")
                return False

            # use minimax choose best move
            best_value = float('-inf') if self.turn == BLACK else float('inf')
            best_piece = None
            best_move = None

            for piece, moves in all_moves.items():
                for move in moves.keys():
                    # Create a temporary board for simulation
                    temp_board = self.board.copy()
                    temp_piece = temp_board.get_piece(piece.row, piece.col)
                    
                    # simulation
                    temp_board.move(temp_piece, move[0], move[1])
                    if moves[move]:  # jump eat
                        temp_board.remove(moves[move])

                    # evaluate
                    value = minimax(
                        temp_board, 3,
                        float('-inf'), float('inf'),
                        True if self.turn == BLACK else False,
                        self, self.turn
                    )[0]

                    # update
                    if (self.turn == BLACK and value > best_value) or \
                       (self.turn == WHITE and value < best_value):
                        best_value = value
                        best_piece = piece
                        best_move = move

            if best_piece and best_move:
                print(f"Kane AI moving piece from ({best_piece.row}, {best_piece.col}) to {best_move}")
                # action
                self.board.move(best_piece, best_move[0], best_move[1])
                
                # jumpeat
                valid_moves = all_moves[best_piece]
                if valid_moves[best_move]:  # if jump eats
                    self.board.remove(valid_moves[best_move])
                    
                    # check continue jump eats
                    next_moves = self.board.get_valid_moves(best_piece)
                    next_jumps = {m: s for m, s in next_moves.items() if s}
                    
                    if next_jumps:
                        print("Additional jumps available")
                        # Recursive processing of consecutive eating skips
                        return self.kane_ai_move()
                
                self.change_turn()
                return True
            else:
                print("Kane AI could not find a valid move")
                return False

        except Exception as e:
            print(f"Error in kane_ai_move: {e}")
            import traceback
            traceback.print_exc()
            return False

    def abel_ai_move(self, ai_instance):
        """handle Abel AI move"""
        try:
            if not ai_instance:
                print("AI instance is None")
                return False
            
            # set current player
            self.board.turn = self.turn  # Make sure the board knows the current player
            
            # Getting AI on the move
            piece, move = ai_instance.predict_move(self.board)
            
            # Check if piece and move are valid
            if piece is None or move is None:
                print("Invalid move returned by AI")
                return False
            
            try:
                print(f"AI move: piece at ({piece.row}, {piece.col}) to {move}")  # debug
            except AttributeError:
                print(f"Invalid piece object: {piece}")
                return False
            
            if piece and move:
                valid_moves = self.board.get_valid_moves(piece)
                print(f"Valid moves for piece: {valid_moves}")  # debug
                
                if valid_moves and move in valid_moves:
                    self.board.move(piece, move[0], move[1])
                    skipped = valid_moves[move]
                    if skipped:
                        self.board.remove(skipped)
                    self.change_turn()
                    return True
                else:
                    print("Move not in valid moves")
            else:
                print("No valid move found")
            return False
        
        except Exception as e:
            print(f"Error in abel_ai_move: {e}")
            import traceback
            traceback.print_exc()  # Print the full error stack
            return False

    def _find_piece_and_move(self, best_move):
     
        old_positions = [(p.row, p.col) for p in self.board.get_all_pieces(self.turn)]
   
        new_positions = [(p.row, p.col) for p in best_move.get_all_pieces(self.turn)]

        piece_pos = [pos for pos in old_positions if pos not in new_positions]
        move_pos = [pos for pos in new_positions if pos not in old_positions]

        if piece_pos and move_pos:
            piece_row, piece_col = piece_pos[0]
            move_row, move_col = move_pos[0]
            return self.board.get_piece(piece_row, piece_col), (move_row, move_col)
        return None, None


## end of code i wrote
