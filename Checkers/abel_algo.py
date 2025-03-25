from stable_baselines3 import PPO
import numpy as np
from Checkers.board import *
import os
import torch
from stable_baselines3.common.vec_env import DummyVecEnv
from CheckersEnv import CheckersEnv
## start of code i wrote
class AbelPPOAI:
    def __init__(self, model_path="abel_final_model"):
        # Load or create a model
        if os.path.exists(f"{model_path}.zip"):
            self.model = PPO.load(model_path)
            print(f"Loaded model from {model_path}")
        else:
            env = CheckersEnv()
            self.model = PPO("MlpPolicy", env, verbose=1)
            print("Created new model")

    def predict_move(self, board):
        """Predicting the next move"""
        try:
            # Creating an Environment 
            env = CheckersEnv()
            env.board = board.copy()
            env.current_player = board.turn if hasattr(board, 'turn') else None
            
            print(f"Current player: {env.current_player}")  # Debugging Information
            
            # Get all moveable pieces of the current player
            valid_pieces = []
            for row in range(8):
                for col in range(8):
                    piece = board.get_piece(row, col)
                    if piece != 0 and piece.color == env.current_player:
                        moves = board.get_valid_moves(piece)
                        if moves:  # If this piece has a legal move
                            valid_pieces.append((piece, moves))
            
            if not valid_pieces:
                print("No valid pieces to move")
                return None, None
            
            # obtain state
            obs = env._get_state()
            
            # obtain ai move
            action, _ = self.model.predict(obs, deterministic=True)
            
            # decode moev
            from_row, from_col, to_row, to_col = env._decode_action(action)
            print(f"Decoded action: from ({from_row}, {from_col}) to ({to_row}, {to_col})")  # Debugging Information
            
            # Verify the validity of the move
            piece = board.get_piece(from_row, from_col)
            if piece:
                print(f"Found piece: color={piece.color}, king={piece.king}")  # Debugging Information
                move = (to_row, to_col)
                valid_moves = board.get_valid_moves(piece)
                print(f"Valid moves for piece: {valid_moves}")  # Debugging Information
                
                if move in valid_moves:
                    return piece, move
                else:
                    print(f"Move {move} not in valid moves {valid_moves}")
                    # If the predicted move is not valid, choose a random valid move
                    piece, moves = valid_pieces[np.random.randint(len(valid_pieces))]
                    move = list(moves.keys())[np.random.randint(len(moves))]
                    return piece, move
            else:
                print(f"No piece found at ({from_row}, {from_col})")
                # If a piece cannot be found, choose a random valid move
                if valid_pieces:
                    piece, moves = valid_pieces[np.random.randint(len(valid_pieces))]
                    move = list(moves.keys())[np.random.randint(len(moves))]
                    return piece, move
            
            return None, None
            
        except Exception as e:
            print(f"Error in predict_move: {e}")
            import traceback
            traceback.print_exc()
            return None, None

    def _board_to_state(self, board):
        """Converting the board to a state representation"""
        state = np.zeros((8, 8, 2), dtype=np.float32)
        
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    state[row, col, 0] = 1 if piece.color == WHITE else -1
                    if piece.king:
                        state[row, col, 1] = 1 if piece.color == WHITE else -1
                        
        return state
## end of code i wrote