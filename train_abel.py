## start of code i wrote
import os
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback
from CheckersEnv import CheckersEnv

def train_abel():
    # Create a directory to store the model
    os.makedirs("models", exist_ok=True)
    os.makedirs("models/checkpoints", exist_ok=True)
    
    # Create a vectorised environment (supports parallel training)
    env = make_vec_env(CheckersEnv, n_envs=4)
    
    # Creating a PPO model
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=1e-4,  # Reduced learning rates
        n_steps=2048,
        batch_size=128,      # Increase batch size
        n_epochs=20,         # Increasing the number of training rounds
        gamma=0.99,          # discount factor
        ent_coef=0.05,      # Increasing the entropy coefficient to increase exploration
        clip_range=0.2,
        policy_kwargs=dict(
            net_arch=[dict(pi=[256, 256], vf=[256, 256])]  # use larger network
        )
    )

    # Create a callback function that saves checkpoints every 10,000 steps.
    checkpoint_callback = CheckpointCallback(
        save_freq=10000,
        save_path="./models/checkpoints/",
        name_prefix="abel_model"
    )

    # start training
    print("Starting training...")
    try:
        model.learn(
            total_timesteps=1000000,  # Increase training steps
            callback=checkpoint_callback
        )
        # Saving the final model
        model.save("models/abel_final_model")
        print("Training completed successfully!")
        
    except Exception as e:
        print(f"Training interrupted: {e}")
        # Saving the model at the time of interruption
        model.save("models/abel_interrupted_model")
        print("Saved interrupted model")

def test_abel(model_path="models/abel_final_model", n_games=5):
    """Testing the trained model"""
    print(f"Testing model from {model_path}")
    
    # load model
    model = PPO.load(model_path)
    env = CheckersEnv()
    
    for game in range(n_games):
        print(f"\nGame {game + 1}")
        obs, _ = env.reset()  # Use only observations, ignore info
        done = False
        total_reward = 0
        moves = 0
        
        while not done:
            # Predictive Action
            action, _ = model.predict(obs, deterministic=True)
            
            # execute an action
            obs, reward, terminated, truncated, info = env.step(action)  # Using the new return value format
            done = terminated or truncated
            total_reward += reward
            moves += 1
            
            # show checkers board
            env.render()
            
            if "invalid_move" in info:
                print("Invalid move detected!")
            
            if done:
                print(f"Game finished after {moves} moves")
                print(f"Total reward: {total_reward}")
                break

def main():
    while True:
        print("\n=== Abel AI Training and Testing ===")
        print("1. Train new model")
        print("2. Test existing model")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            train_abel()
        elif choice == '2':
            # check model file
            models_dir = "models"
            if not os.path.exists(models_dir):
                print("No models directory found!")
                continue
                
            models = [f for f in os.listdir(models_dir) if f.endswith('.zip')]
            if not models:
                print("No trained models found!")
                continue
                
            print("\nAvailable models:")
            for i, model in enumerate(models):
                print(f"{i+1}. {model}")
            
            try:
                model_idx = int(input("Select model number (or press Enter for latest): ")) - 1
                model_path = os.path.join(models_dir, models[model_idx])
            except:
                model_path = os.path.join(models_dir, models[-1])
                print(f"Using latest model: {models[-1]}")
            
            n_games = input("Enter number of test games (default 5): ")
            n_games = int(n_games) if n_games.isdigit() else 5
            
            test_abel(model_path, n_games)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
## end of code i wrote