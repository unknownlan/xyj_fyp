## start of code i wrote
import matplotlib.pyplot as plt
import sys
import os

# Add the main_board.py directory to PYTHONPATH.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main_board import main_board

class KaneVsAbelEvaluator:
    def __init__(self, num_games=50):
        self.num_games = num_games
        self.kane_wins = 0
        self.abel_wins = 0

    def evaluate(self):
        for game in range(self.num_games):
            print(f"Starting game {game + 1}")
            winner = main_board(3, white_type='Kane', black_type='Kane')
            if winner == 'WHITE':
                self.kane_wins += 1
            elif winner == 'BLACK':
                self.abel_wins += 1

        self.plot_results()

    def plot_results(self):
        """Charting the number of wins"""
        labels = ['Kane (White)', 'Kane (Black)']
        wins = [self.kane_wins, self.abel_wins]

        plt.figure(figsize=(4, 6))
        plt.bar(labels, wins, color=['blue', 'red'])
        plt.title('Kane vs Kane - Wins after 50 Games')
        plt.xlabel('AI Player')
        plt.ylabel('Number of Wins')
        plt.ylim(0, self.num_games)
        plt.grid(axis='y')
        plt.savefig('kane_vs_kane.png')
        plt.show()

def main():
    evaluator = KaneVsAbelEvaluator(num_games=50)
    evaluator.evaluate()

if __name__ == "__main__":
    main() 

## end of code i wrote