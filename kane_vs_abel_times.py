## start of code i wrote
import time
import matplotlib.pyplot as plt
from main_board import main_board

class DecisionTimeEvaluator:
    def __init__(self):
        self.kane_times = []
        self.abel_times = []

    def record_think_time(self, start_time, player):
        """Record thinking time for each step"""
        think_time = time.time() - start_time
        if player == 'WHITE':
            self.kane_times.append(think_time)
        elif player == 'BLACK':
            self.abel_times.append(think_time)

    def evaluate(self):
        print("Starting game")
        main_board(3, white_type='Kane', black_type='Abel', callback=self.record_think_time)
        self.plot_think_times()

    def plot_think_times(self):
        """Charting thinking time"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.kane_times, marker='o', label='Kane (White)')
        plt.plot(self.abel_times, marker='x', label='Abel (Black)')
        plt.title('Kane vs Abel - Decision Times')
        plt.xlabel('Move Number')
        plt.ylabel('Think Time (seconds)')
        plt.legend()
        plt.grid(True)
        plt.savefig('kane_vs_abel_decision_times.png')
        plt.show()

def main():
    evaluator = DecisionTimeEvaluator()
    evaluator.evaluate()

if __name__ == "__main__":
    main() 

## end of code i wrote