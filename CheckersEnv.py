## start of code i wrote
import gymnasium as gym
import numpy as np
from gymnasium import spaces
from Checkers.constants import WHITE, BLACK
from Checkers.board import Board

class CheckersEnv(gym.Env):
    def __init__(self):
        super().__init__()
        
        self.board = Board()
        self.current_player = BLACK
        
        # Modify action space to discrete space
        # Possible moves from each position to other positions
        self.action_space = spaces.Discrete(8 * 8 * 4)  # Up to 4 directions per position
        
        # observation space: 8x8x3
        # Channel 1: Current player's piece (1 is a normal piece, 2 is a king)
        # Channel 2: Opponent's pieces (1 is a normal piece, 2 is a king)
        # Channel 3: Moveable marker (1 means that the piece in this position can be moved)
        self.observation_space = spaces.Box(
            low=0, high=2,
            shape=(8, 8, 3),
            dtype=np.float32
        )
        
        self.invalid_moves_count = 0
        self.max_invalid_moves = 20  # Reduces the maximum number of ineffective moves
        self.move_history = []  # Add movement History
        self.max_history_length = 10  # save recent 10 moves
        
        # Stores all possible directions of movement
        self.directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    def _decode_action(self, action_number):
        """Decode action figures into specific movements"""
        # First get all the moveable pieces of the current player.
        valid_pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == self.current_player:
                    moves = self.board.get_valid_moves(piece)
                    if moves:  # If this piece has a legal move
                        valid_pieces.append((piece, moves))
        
        if not valid_pieces:  # If this piece is not a legal move
            return 0, 0, 0, 0
        
        # Preferred Jump Eat Move
        jump_moves = []
        for piece, moves in valid_pieces:
            for move, skip in moves.items():
                if skip:  # If it's a jump eat move
                    jump_moves.append((piece, move))
        
        # If there is a skip-eat move, select one from it
        if jump_moves:
            piece_idx = action_number % len(jump_moves)
            piece, move = jump_moves[piece_idx]
            return piece.row, piece.col, move[0], move[1]
        
        # If there is not a skip-eat move, select one legal move
        all_moves = []
        for piece, moves in valid_pieces:
            for move in moves.keys():
                all_moves.append((piece, move))
        
        if all_moves:
            piece_idx = action_number % len(all_moves)
            piece, move = all_moves[piece_idx]
            return piece.row, piece.col, move[0], move[1]
        
        return 0, 0, 0, 0  # If no legal movement is found

    def reset(self, seed=None, options=None):
        """reset environment"""
        super().reset(seed=seed)
        
        self.board = Board()
        self.current_player = BLACK
        self.invalid_moves_count = 0  # Reset Invalid Move Count
        self.move_history = []  # Reset Move History
        return self._get_state(), {}

    def step(self, action):
        """Perform a one-step action"""
        # decode an action
        from_row, from_col, to_row, to_col = self._decode_action(action)
        
        # Get Selected Pieces
        piece = self.board.get_piece(from_row, from_col)
        
        # Checking the legality of actions
        if not piece or piece.color != self.current_player:
            self.invalid_moves_count += 1
            if self.invalid_moves_count >= self.max_invalid_moves:
                return self._get_state(), -50, True, False, {"invalid_move": True}
            return self._get_state(), -1, False, False, {"invalid_move": True}
            
        # Getting legal movement
        valid_moves = self.board.get_valid_moves(piece)
        move = (to_row, to_col)
        
        # If the move is not legal
        if move not in valid_moves:
            self.invalid_moves_count += 1
            if self.invalid_moves_count >= self.max_invalid_moves:
                return self._get_state(), -50, True, False, {"invalid_move": True}
            return self._get_state(), -1, False, False, {"invalid_move": True}
            
        # Check if it is a duplicate move
        current_move = (from_row, from_col, to_row, to_col)
        if len(self.move_history) >= 4:  # check recent 4 move
            if self._is_repetitive_move(current_move):
                return self._get_state(), -10, False, False, {"repetitive_move": True}
        
        # update move history
        self.move_history.append(current_move)
        if len(self.move_history) > self.max_history_length:
            self.move_history.pop(0)
        
        # Reset Invalid Move Count
        self.invalid_moves_count = 0
        reward = 0
        
        # Execute the move
        self.board.move(piece, to_row, to_col)
        
        # Basic Movement Bonus
        reward += 0.1
        
        # resort to skipping meals
        skipped = valid_moves.get(move)
        if skipped:
            self.board.remove(skipped)
            reward += 5  # Increase Jump Eat Reward
            
            # Check if it is possible to skip eating continuously
            next_moves = self.board.get_valid_moves(piece)
            if any(skip for _, skip in next_moves.items()):
                reward += 2  # Reward possible consecutive jumps to eat
        
        # handel kings
        if piece.king:
            reward += 0.2  # king move rewards
        elif (piece.color == WHITE and to_row == 0) or (piece.color == BLACK and to_row == 7):
            piece.make_king()
            reward += 3
        
        # Positional incentives: encourage movement towards the opponent's area
        if piece.color == BLACK:
            reward += (to_row - from_row) * 0.1  # Move down to get a positive bonus
        else:
            reward += (from_row - to_row) * 0.1  # Move up to get a positive bonus
        
        # Check if the game is over
        winner = self.board.winner()
        done = winner is not None
        
        if done:
            if winner == self.current_player:
                reward += 20
            else:
                reward -= 20
                
        # change player
        self.current_player = WHITE if self.current_player == BLACK else BLACK
        
        return self._get_state(), reward, done, False, {}

    def _is_repetitive_move(self, current_move):
        """check repeat move"""
        if len(self.move_history) < 4:
            return False
            
        # Check if it's moving back and forth
        last_moves = self.move_history[-4:]
        for i in range(len(last_moves)-1):
            if (last_moves[i][0] == current_move[2] and 
                last_moves[i][1] == current_move[3] and
                last_moves[i][2] == current_move[0] and
                last_moves[i][3] == current_move[1]):
                return True
        return False

    def _get_state(self):
        """Get current state"""
        state = np.zeros((8, 8, 3), dtype=np.float32)  # change channel 3
        
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece != 0:
                    # Channel 0: Current player's normal piece
                    # Channel 1: Current Player's King Pawn
                    # Channel 2: Opponent's discs (including normal discs and king pieces)
                    if piece.color == self.current_player:
                        if piece.king:
                            state[row, col, 1] = 1
                        else:
                            state[row, col, 0] = 1
                    else:
                        state[row, col, 2] = 1
        
        return state

    def render(self):
        """Rendering the board"""
        print("\nCurrent board state:")
        print(f"Current player: {'BLACK' if self.current_player == BLACK else 'WHITE'}")
        print(f"Invalid moves count: {self.invalid_moves_count}")
        print(self.board)

## end of code i wrote