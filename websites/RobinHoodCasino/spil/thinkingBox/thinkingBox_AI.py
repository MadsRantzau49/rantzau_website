import random
import numpy as np
from collections import defaultdict
import gym
from gym import spaces
import pickle
import logging
import time
from print_data import *



# Constants
<<<<<<< HEAD
NUM_TRAIN_AI = 10
=======
NUM_TRAIN_AI = 5
>>>>>>> origin/main
START_DICE_AMOUNT = 4
PLAYERS_AMOUNT = 2
PLOT_DATA = True


# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Adjust this to INFO or WARNING to reduce verbosity
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data/game_bot.log", mode="w"),
        # logging.StreamHandler()
    ]
)

logger = logging.getLogger('GameBot')


# Plotgraps:
max_amount = (START_DICE_AMOUNT + 1) * PLAYERS_AMOUNT
max_dices = START_DICE_AMOUNT * PLAYERS_AMOUNT
# Action space: all the possible calls + 1 (0) for calling bluff
MAX_OPTIONS = PLAYERS_AMOUNT * (START_DICE_AMOUNT + 1) * 7


# ----------------------------------------------------------------------------------------------------Setup

map_call = {index + 1: [i + 1, y] for i in range(max_amount) for index, y in enumerate(["k"] + [str(x) for x in range(1, 7)], start=i*7)}
map_call[0] = "lift"

plot_action = {y: {key: [0,0,0] for key in map_call} for y in range(2,max_dices+1)}
class PlayerInformation:
    def __init__(self, player_id: int, dice_amount: int):
        self.id = player_id
        self.dice_amount = dice_amount
        self.dice_roll = []

class ThinkingBoxEnv(gym.Env):
    def __init__(self):
        super(ThinkingBoxEnv, self).__init__()
        

        self.action_space = spaces.Discrete(MAX_OPTIONS + 1)
        
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
            logger.info(f"DICEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE Player {player.id} dice: {player.dice_roll}")

    def get_state(self):
        # Initialize the state list with the current player
        state = []

        # Add the last guess information
        if self.last_guess:
            amount, guess_value = self.last_guess
            state.extend([amount, 7 if guess_value == 'k' else int(guess_value)])
        else:
            state.extend([0, 0])

        # Add the number of dice each player has
        state.extend([player.dice_amount for player in self.players])

        current_len = len(state)

        # Add the dice rolls for the current player
        for player in self.players:
            if player.id == self.current_player:
                state.extend(player.dice_roll)
        
        #ensure that the length is always equal by adding 0 until its full (maybe stupid)
        while len(state) != (current_len + START_DICE_AMOUNT):
            state.extend([0])

        # Convert to NumPy array
        # state = [guessAmount, guessValue, player1dicesremaining,player2RicesRemaining, currentPlayerDiceRoll ]
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

    def check_for_max_guess(self, guess):
        amountOfDices = sum(player.dice_amount + 1 for player in self.players)
        amount, value = guess
        return amount == amountOfDices and value == "6"
    
    def step(self, action):
        logger.info(f"player {self.current_player} chooses action = {map_call[action]}")
        done = False
        reward = 0
        dice_amount_back = sum(player.dice_amount for player in self.players)
        plot_action[dice_amount_back][action][0] += 1
        if action == 0:  # Lift
            if not self.last_guess:
                reward -= 1000  # Penalty for invalid action
                plot_action[dice_amount_back][action][2] += 1
                logger.info(f"player {self.current_player} lifted when no guess made yet. Cannot call a bluff and looses.")
                self.player_lost(self.current_player)
            else:
                if self.guess_is_true(self.last_guess):
                    reward -= 1
                    plot_action[dice_amount_back][action][2] += 1
                    logger.info(f"Player {self.current_player} Failed Lift")
                    self.player_lost(self.current_player)          
                else:
                    reward += 1
                    plot_action[dice_amount_back][action][1] += 1
                    logger.info(f"Player {self.current_player} Correct Lift")
                    self.player_lost(self.last_player)
        
        else: #Take a guess
            if self.last_guess and self.check_for_max_guess(self.last_guess):
                reward -= 10
                plot_action[dice_amount_back][action][2] += 1
                logger.info(f"player {self.current_player} You lost cause you rolled when your opp tried everybody has the stairs, IDIOT")
                self.player_lost(self.current_player)
            else:
                guess = map_call[action]
                if not self.validGuess(guess):
                    reward -= 10
                    plot_action[dice_amount_back][action][2] += 1
                    logger.info(f"player {self.current_player} make a invalid guess and therefore lost. The guess {guess}")
                    self.player_lost(self.current_player)
                else:
                    reward += 1
                    if self.guess_is_true(guess):
                        reward += guess[0]** 5
                        plot_action[dice_amount_back][action][1] += 1
                        logger.debug(f"player {self.current_player} make a valid guess and rewarded: {reward} ")
                    else:
                        reward -= 1
                        plot_action[dice_amount_back][action][2] += 1
                        logger.debug(f"player{self.current_player} make a valid but fail call, gotta hope the next person doesnt lift")
                        
                    self.last_player = self.current_player
                    self.current_player = self.next_player()
                    self.last_guess = guess
                                    
        self.state = self.get_state()

        if self.check_game_done():
            logger.info("GAME IS DONE")
            done = True
        
        logger.debug(f"State: {self.state}, Reward: {reward}")
        logger.info("")
        return self.state, reward, done, {}

    def make_guess(self):
        amountOfDices = sum(player.dice_amount + 1 for player in self.players)

        # amount = round(random.triangular(1, amountOfDices, 1))
        amount = random.randint(1,amountOfDices)
        guess_value = random.choice([str(i) for i in range(1, 7)] + ["k"])
        return [amount, guess_value]

    def guess_is_true(self, guess):
        result = self.count_all_dices(self.players)
        amount, guess_value = guess
        logger.debug(result)
        # print(f"amount{amount}, guess:{guess_value}")
        if guess_value == "k":
            if amount == 1:
                logger.debug(f"expression: result[guess_value] <= amount:: {result[guess_value] <= amount}, amount= {amount}, result= {result[guess_value]}")
            return result[guess_value] >= amount
        return result[int(guess_value)] >= amount

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

    def check_for_straight(self, dice_roll: list) -> bool:
        return sorted(dice_roll) == list(range(1, len(dice_roll) + 1))

    def count_all_dices(self, players: list) -> dict:
        result = {i: 0 for i in range(1, 7)}
        for player in players:
            if player.dice_amount == 0:
                continue
            if self.check_for_straight(player.dice_roll):
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
<<<<<<< HEAD
    def __init__(self, state_space, action_space, alpha=0.1, gamma=0.99, epsilon=0.0):
=======
    def __init__(self, state_space, action_space, alpha=0.1, gamma=0.99, epsilon=0):
>>>>>>> origin/main
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
    env = ThinkingBoxEnv()
    agent = QLearningAgent(env.observation_space, env.action_space)

    # Load previously saved Q-table if it exists
    load_q_table(agent, 'data/q_table.pkl')

    num_episodes = NUM_TRAIN_AI

    for episode in range(num_episodes):
        start_time = time.time()
        if episode % 1000 == 0: print(episode)
        state = env.reset()
        done = False
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.learn(state, action, reward, next_state)
            state = next_state
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.debug(f"One game takes {elapsed_time} seconds")

    # Save Q-table after training
    save_q_table(agent, 'data/q_table.pkl')

def play_game():
    env = ThinkingBoxEnv()
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
                print(f"AI choooooooooooooooooose to play: {action}")
                if action == 0:  # Make a guess
                    # ONLY TRAINING
                    lost = False
                    if env.last_guess:
                        if env.check_for_max_guess(env.last_guess):
                            print("You lost cause you rolled when your opp tried everybody has the stairs, IDIOT")
                            env.player_lost(env.current_player)
               
                    if not lost:
                        guess = env.make_guess()
                        while not env.validGuess(guess):
                            guess = env.make_guess()
                        env.last_player = env.current_player
                        env.current_player = env.next_player()
                        env.last_guess = guess
                        print(f"Player {env.current_player} makes a guess: {guess}")
                
                elif action == 1:  # Call a bluff
                    if env.last_guess is None:
                        print("No guess made yet. Cannot call a bluff.")
                        env.player_lost(env.current_player)
                    else:
                        if env.guess_is_true(env.last_guess):
                            logger.info(f"Player {env.current_player} calls bluff correctly.")
                            env.player_lost(env.last_player)          
                        else:
                            logger.info(f"Player {env.current_player} calls bluff incorrectly.")
                            env.player_lost(env.current_player)

            done = env.check_game_done()            
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
        start_time = time.time()
        train_agent()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.4f} seconds to execute {NUM_TRAIN_AI} games")

    elif choice == '2':
        print("Playing against the AI...")
        play_game()
    else:
        print("Invalid choice. Exiting.")

    if PLOT_DATA:
        logger.debug("Pl")
        start_time = time.time()
        plot_action_into_chart(max_dices,plot_action,map_call,MAX_OPTIONS)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.4f} seconds to plot data")

   

if __name__ == "__main__":
    main()


