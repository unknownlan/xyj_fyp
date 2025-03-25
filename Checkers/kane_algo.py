## start of code i wrote
from .constants import WHITE, BLACK, RED
import pygame
import time
import random

# settings
MAX_DEPTH = 10
MAX_MOVES = 4  # Reduction in the number of moves considered
USE_CACHE = False  # Disable caching to reduce memory usage

# Add a history of moves to avoid duplicates
last_moves = []
MAX_HISTORY = 6  # Record the last 6 steps

def minimax(position, depth, alpha, beta, max_player, game, color, callback=None):
    """Minimalist Minimax Algorithm"""
    start_time = time.time()
    
    # Immediate return of assessed value
    if depth == 0 or position.winner() is not None:
        if callback:
            callback(start_time)
        return position.evaluate(), position

    # Get the current player's colour
    current_color = color if max_player else (WHITE if color == BLACK else BLACK)
    
    # Getting and limiting the number of moves
    moves = get_first_moves(position, current_color)
    if not moves:
        if callback:
            callback(start_time)
        return position.evaluate(), position

    # If there is only one piece left, randomly select the move
    if len(position.get_all_pieces(current_color)) == 1:
        # avoid repeat move
        valid_moves = [m for m in moves if not is_repeated_move(position, m)]
        if valid_moves:
            best_move = random.choice(valid_moves)
            evaluation = evaluate_board(best_move, color)
            if callback:
                callback(start_time)
            return evaluation, best_move
        # If all moves are duplicates, select a random move
        best_move = random.choice(moves)
        evaluation = evaluate_board(best_move, color)
        if callback:
            callback(start_time)
        return evaluation, best_move

    best_move = moves[0]
    if max_player:
        maxEval = float('-inf')
        for move in moves:
            evaluation = evaluate_board(move, color)
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
        if callback:
            callback(start_time)
        return maxEval, best_move
    else:
        minEval = float('inf')
        for move in moves:
            evaluation = evaluate_board(move, color)
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
        if callback:
            callback(start_time)
        return minEval, best_move

def is_repeated_move(old_board, new_board):
    """Check if it is a duplicate move"""
    board_state = str(new_board)
    if board_state in last_moves:
        return True
    return False

def update_move_history(board):
    """Update Move History"""
    global last_moves
    board_state = str(board)
    last_moves.append(board_state)
    if len(last_moves) > MAX_HISTORY:
        last_moves.pop(0)

def get_first_moves(board, color):
    """Get the first few possible moves"""
    moves = []
    pieces = board.get_all_pieces(color)
    
    # Prioritise Jump Eat Move
    for piece in pieces:
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if skip:  # Jump Eat
                temp_board = simulate_move(piece, move, board, skip)
                moves.append(temp_board)
                if len(moves) >= MAX_MOVES:
                    return moves

    # If there are no jump eats, consider normal movement
    if not moves:
        for piece in pieces:
            valid_moves = board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                temp_board = simulate_move(piece, move, board, skip)
                moves.append(temp_board)
                if len(moves) >= MAX_MOVES:
                    return moves

    # If there is only one piece, randomly disrupt the move order
    if len(pieces) == 1:
        random.shuffle(moves)
    
    return moves

def simulate_move(piece, move, board, skip):
    """Simple movement simulation"""
    temp_board = board.copy()
    temp_piece = temp_board.get_piece(piece.row, piece.col)
    if temp_piece:
        temp_board.move(temp_piece, move[0], move[1])
        if skip:
            temp_board.remove(skip)
    return temp_board

def evaluate_board(board, color):
    """Quick Evaluation Functions"""
    opponent = WHITE if color == BLACK else BLACK
    
    # Calculation of basic scores
    score = 0
    
    # Difference in number of pieces
    score += len(board.get_all_pieces(color)) * 10
    score -= len(board.get_all_pieces(opponent)) * 10
    
    # Simple location assessment
    for piece in board.get_all_pieces(color):
        if color == BLACK:
            score += (7 - piece.row)  
        else:
            score += piece.row  
            
    # Add a randomisation factor to avoid repetitive movements
    score += random.uniform(-0.5, 0.5)
            
    return score

def move_minimax(old_board, new_board, color):
    """Simple Motion Detection"""
    if not new_board or not old_board:
        return None, None, None, None

    try:
        # Get the position before and after the move
        old_pieces = [(p.row, p.col) for p in old_board.get_all_pieces(color)]
        new_pieces = [(p.row, p.col) for p in new_board.get_all_pieces(color)]
        
        # Find the location of the change
        for old_pos in old_pieces:
            if old_pos not in new_pieces:
                for new_pos in new_pieces:
                    if new_pos not in old_pieces:
                        # update history
                        update_move_history(new_board)
                        return old_pos[0], old_pos[1], new_pos[0], new_pos[1]
                        
    except Exception as e:
        print(f"Error in move_minimax: {e}")
    
    return None, None, None, None

def draw_moves(game, board, piece):
    """Plotting possible moves"""
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, RED, (piece.x, piece.y), 30, 2)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()

## end of code i wrote


