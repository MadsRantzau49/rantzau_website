import random
import numpy as np
from collections import defaultdict
import gym
from gym import spaces
import pickle

# Constants
START_DICE_AMOUNT = 4
PLAYERS_AMOUNT = 2

# ----------------------------------------------------------------------------------------------------Setup

class PlayerInformation:
    def __init__(self, player_id: int, dice_amount: int):
        self.id = player_id
        self.dice_amount = dice_amount
        self.dice_roll = []

class DanishDiceGameEnv(gym.Env):
    def __init__(self):
        super(DanishDiceGameEnv, self).__init__()
        
        # Action space: 2 actions (0: Make a guess, 1: Call a bluff)
        self.action_space = spaces.Discrete(2)
        
        # Observation space: Flattened state representation
        self.observation_space = spaces.Box(low=0, high=7, shape=(2 + 2 * PLAYERS_AMOUNT,), dtype=np.int32)
        
        # self.reset()

    def reset(self):
        self.players = [PlayerInformation(i, START_DICE_AMOUNT) for i in range(PLAYERS_AMOUNT)]
        self.current_player = 0
        self.last_player = None
        self.last_guess = None
        self.roll_dice_for_all_players()
        self.state = self.get_state()
        # print(f"Game reset. Starting state: {self.state}")
        return self.state

    def roll_dice_for_all_players(self):
        for player in self.players:
            if player.dice_amount > 0:
                player.dice_roll = [random.randint(1, 6) for _ in range(player.dice_amount)]
        self.print_dice_info()
    
    def print_dice_info(self):
        for player in self.players:
            print(f"Player {player.id} dice: {player.dice_roll}")

    def get_state(self):
        # Flattened state: [current_player, last_guess_amount, last_guess_value, player1_dice_amount, player2_dice_amount, ...]
        state = [self.current_player]
        if self.last_guess:
            amount, guess_value = self.last_guess
            state.extend([amount, 7 if guess_value == 'k' else int(guess_value)])
        else:
            state.extend([0, 0])
        state.extend([player.dice_amount for player in self.players])
        return np.array(state, dtype=np.int32)

    def next_player(self):
        for player in self.players:
            for i in range(1,len(self.players)):
                if player.id == (player.id + i) and player.dice_amount > 0:
                    return player.id
        for player in self.players:
            if player.dice_amount > 0 and player.id != self.current_player:
                return player.id
            
    def remove_dice(self,loosingPlayer):
        for player in self.players:
            if player.id != loosingPlayer:
                player.dice_amount = max(0, player.dice_amount - 1)
    
    def player_lost(self, loosingPlayer):
        self.remove_dice(loosingPlayer)
        self.roll_dice_for_all_players()
        self.current_player = loosingPlayer
        self.last_player = None
        self.last_guess = None

    
    def step(self, action):
        done = False
        reward = 0

        if action == 0:  # Make a guess
            guess = self.make_guess()
            print(f"Player {self.current_player} makes a guess: {guess}")
            if not self.validGuess(self.last_guess):
                reward = -1
                print(f"player {self.current_player} make a unvalid guess")
                self.player_lost(self.current_player)
            else:
                self.last_player = self.current_player
                self.current_player = self.next_player()
                self.last_guess = guess

        elif action == 1:  # Call a bluff
            if self.last_guess is None:
                reward = -1  # Penalty for invalid action
                print("No guess made yet. Cannot call a bluff.")
            else:
                if self.guess_is_true(self.last_guess):
                    reward = 1
                    print(f"Player {self.current_player} calls bluff correctly.")
                    self.player_lost(self.last_player)          
                else:
                    reward = -1
                    print(f"Player {self.current_player} calls bluff incorrectly.")
                    self.player_lost(self.current_player)
                                    
        self.state = self.get_state()
        # print(f"New state: {self.state}")

        if self.check_game_done():
            print("GAME IS DONE")
            done = True
            reward = -10  # Higher penalty for losing the game

        return self.state, reward, done, {}

    def make_guess(self):
        amountOfDices = sum(player.dice_amount + 1 for player in self.players) + 1
        amount = random.randint(1, amountOfDices)
        guess_value = random.choice([str(i) for i in range(1, 7)] + ["k"])
        return [amount, guess_value]

    def guess_is_true(self, guess):
        result = count_all_dices(self.players)
        amount, guess_value = guess
        # print(result)
        # print(f"amount{amount}, guess:{guess_value}")
        if guess_value == "k":
            return result[guess_value] <= amount
        return result[int(guess_value)] <= amount

    def validGuess(self, guess):
        if not self.last_guess:
            return True
        amount, guess_value = guess
        last_amount, last_guess_value = self.last_guess
        if amount < last_amount:
            return False
        
        if guess == self.last_guess:
            return False
        
        if amount > last_amount:
            return True
        
        if amount == last_amount:
            if last_guess_value == "k":
                return True
            
            if guess_value == "k":
                return False
            
            if guess_value < last_guess_value:
                return False
        return True

    def check_game_done(self):
        # The game is done if only one player has dice left
        players_with_dice = sum(1 for player in self.players if player.dice_amount > 0)
        return players_with_dice <= 1

def check_for_straight(dice_roll: list) -> bool:
    return sorted(dice_roll) == list(range(1, len(dice_roll) + 1))

def count_all_dices(players: list) -> dict:
    result = {i: 0 for i in range(1, 7)}
    for player in players:
        if player.dice_amount == 0:
            continue
        if check_for_straight(player.dice_roll):
            for d in result:
                result[d] += len(player.dice_roll) + 1
        else:
            for dice in player.dice_roll:
                result[dice] += 1
                if dice == 1:
                    result = {k: v + 1 for k, v in result.items()}
                    result[1] -= 1
    result["k"] = max(result.values())    
    return result

# Q-learning Agent
class QLearningAgent:
    def __init__(self, state_space, action_space, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.state_space = state_space
        self.action_space = action_space
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = defaultdict(lambda: np.zeros(self.action_space.n))

    def choose_action(self, state):
        state_tuple = tuple(state)
        if random.uniform(0, 1) < self.epsilon:
            action = self.action_space.sample()  # Explore
            # print(f"Choosing random action: {action}")
        else:
            action = np.argmax(self.q_table[state_tuple])  # Exploit
            # print(f"Choosing best action based on Q-values: {action}")
        return action

    def learn(self, state, action, reward, next_state):
        state_tuple = tuple(state)
        next_state_tuple = tuple(next_state)
        
        best_next_action = np.argmax(self.q_table[next_state_tuple])
        td_target = reward + self.gamma * self.q_table[next_state_tuple][best_next_action]
        td_error = td_target - self.q_table[state_tuple][action]
        self.q_table[state_tuple][action] += self.alpha * td_error
        # print(f"Updated Q-value for state {state}, action {action}: {self.q_table[state_tuple][action]}")

def save_q_table(agent, filename):
    with open(filename, 'wb') as file:
        pickle.dump(dict(agent.q_table), file)  # Convert defaultdict to dict
    # print(f"Q-table saved to {filename}")

def load_q_table(agent, filename):
    try:
        with open(filename, 'rb') as file:
            agent.q_table = defaultdict(lambda: np.zeros(agent.action_space.n), pickle.load(file))
        # print(f"Q-table loaded from {filename}")
    except FileNotFoundError:
        print(f"No Q-table file found at {filename}, starting with a new Q-table.")

def train_agent():
    env = DanishDiceGameEnv()
    agent = QLearningAgent(env.observation_space, env.action_space)

    # Load previously saved Q-table if it exists
    load_q_table(agent, 'q_table.pkl')

    num_episodes = 1

    for episode in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state

    # Save Q-table after training
    save_q_table(agent, 'q_table.pkl')

def play_game():
    env = DanishDiceGameEnv()
    agent = QLearningAgent(env.observation_space, env.action_space)

    # Load the trained Q-table
    load_q_table(agent, 'q_table.pkl')

    # Choose which player you want to control
    player_choice = int(input("Choose your player (0 or 1): "))
    if player_choice not in [0, 1]:
        print("Invalid choice. Exiting.")
        return

    while True:
        state = env.reset()
        done = False
        while not done:
            if env.current_player == player_choice:
                action = int(input("Choose action (0: Make a guess, 1: Call a bluff): ").strip())
                if action == 0:
                    amount = int(input("Enter the guessed amount (1-6): ").strip())
                    guess_value = input("Enter the guessed value (1-6 or 'k' for straight): ").strip()
                    if guess_value not in [str(i) for i in range(1, 7)] + ["k"]:
                        print("Invalid guess value.")
                        continue
                    if not env.validGuess([amount, guess_value]):
                        env.player_lost(env.current_player)
                    else:
                        env.last_guess = [amount, guess_value]
                        env.last_player = env.current_player
                        env.current_player = env.next_player()
                elif action == 1:
                    if env.guess_is_true(env.last_guess):
                        env.player_lost(env.last_player) 
                    else:
                        env.player_lost(env.current_player)
            else:
                action = agent.choose_action(state)
                if action == 0:
                    guess = env.make_guess()

                    print(f"AI makes a guess: {guess}")
                    if not env.validGuess(guess):
                        env.player_lost(env.current_player)
                    else:
                        env.last_guess = guess
                        env.last_player = env.current_player
                        env.current_player = env.next_player()
                elif action == 1:
                    if env.last_guess is None:
                        print("AI cannot call a bluff as no guess has been made yet.")
                    else:
                        if env.guess_is_true(env.last_guess):
                            env.player_lost(env.last_player) 
                        else:
                            env.player_lost(env.current_player)
            done = env.check_game_done()            
            print(done)
            if done:
                print("Game over.")
                break

def main():
    print("Choose an option:")
    print("1: Train the AI")
    print("2: Play against the AI")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == '1':
        print("Training the AI...")
        train_agent()
    elif choice == '2':
        print("Playing against the AI...")
        play_game()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
