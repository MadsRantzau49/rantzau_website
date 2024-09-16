from collections import Counter


# state = [guessAmount, guessValue, player1dicesremaining,player2RicesRemaining, currentPlayerDiceRoll ]

class RantzauBestStrategy:

    def main(state):
        guessAmount, guessValue, p1DiceCount, p2DiceCount, d1,d2,d3,d4 = state
        dices = [d1,d2,d3,d4]
        maxbet = RantzauBestStrategy.maxBet(dices)
        print(maxbet)


    def maxBet(dices):
        # Initialize an empty dictionary to store frequencies
        frequency = {}

        # Count the occurrences of each element
        for num in dices:
            if num in frequency:
                frequency[num] += 1
            else:
                frequency[num] = 1

        # Find the maximum frequency
        max_frequency = max(frequency.values())

        # Filter elements that have the maximum frequency
        candidates = [num for num, freq in frequency.items() if freq == max_frequency]

        # Select the highest element among the candidates
        most_common_element = max(candidates)

        return most_common_element
state = [4, 7, 4, 4, 5, 3, 5, 3]
RantzauBestStrategy.main(state)