# Kane and Abel， AI that plays game
The project Kane and Abel: AIs that Play Games explores two distinct approaches to artificial intelligence in game-playing. Kane, the first AI, is based on a pre-programmed set of rules and logic, designed to simulate decision-making in a structured environment like Western checkers. It uses fixed strategies and does not adapt or learn from its experiences. In contrast, Abel is a machine learning-powered AI that uses reinforcement learning to adapt and improve over time. Abel learns from its interactions with the game environment, constantly refining its gameplay to make more effective moves.


## Table of Contents
- [Installation](#installation)
- [Technologies](#technologies)
- [Acknowledgments](#acknowledgments)
- [Modifications](#modifications)

## Installation

1. Navigate to the project directory:
    ```bash
    cd checkers-pygame-main
    ```

2. Install the required dependency (Pygame):
    ```bash
    pip install pygame
    ```

3. Run the game:
    ```bash
    python main.py
    ```
## Technologies
- **Python**: The programming language used for the game logic.
- **Pygame**: Used for rendering the game window and handling input/output.
- **Gymnasium**: A toolkit for developing and comparing reinforcement learning environments.
- **Stable-Baselines3**: A library that provides implementations of popular RL algorithms.
- **Torch**: A deep learning framework used for building and training models.
- **Numpy**: A library for numerical computing in Python, used for handling arrays and mathematical functions.
- **Shimmy**: A library for connecting reinforcement learning environments to stable-baselines3.
- **Seaborn**: A data visualization library based on matplotlib, used for plotting graphs and analysis.

## Acknowledgments 
This project is based on [checkers-pygame](https://github.com/psycocodes/checkers-pygame).  
To differentiate my modifications, i have marked the custom-written code with the following comments in the source files: 
“## start of code i wrote” and "## end of code i wrote"

### Modifications  
I have made the following enhancements to the original code:  
- Implemented Kane  using the Minimax algorithm with alpha-beta pruning.  
- Implemented Abel and its training environment.
- Improved the game logic and UI for better usability. 
- Testing and iterations.




