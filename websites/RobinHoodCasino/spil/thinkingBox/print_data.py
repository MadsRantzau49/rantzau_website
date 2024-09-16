import matplotlib
matplotlib.use('Agg')  # Use the Agg backend

import matplotlib.pyplot as plt
import numpy as np

def plot_action_into_chart(max_dices, plot_action, map_call, MAX_OPTIONS):
    for i in range(2, max_dices + 1):
        # Prepare the data for plotting
        x_labels = []
        y_values_0 = []  # action
        y_values_1 = []  # good
        y_values_2 = []  # bad

        for j in range(len(plot_action[i])):
            x_labels.append(str(map_call[j]))
            y_values_0.append(plot_action[i][j][0])
            y_values_1.append(plot_action[i][j][1])
            y_values_2.append(plot_action[i][j][2])

        fig, ax = plt.subplots(figsize=(12, 6))  # Increase figure size

        index = np.arange(len(x_labels))
        bar_width = 0.2  # Adjust bar width
        group_spacing = 0.1  # Increase spacing between groups

        # Define bar positions for each category with additional spacing between groups
        bars1 = ax.bar(index - bar_width - group_spacing/2, y_values_0, bar_width, label='action', color='black')
        bars2 = ax.bar(index, y_values_1, bar_width, label='good', color='green')
        bars3 = ax.bar(index + bar_width + group_spacing/2, y_values_2, bar_width, label='bad', color='red')

        ax.set_xlabel('X Labels', fontsize=10)  # Adjust font size
        ax.set_ylabel('Values', fontsize=10)  # Adjust font size
        ax.set_title(f'Plot for {i} Dices', fontsize=12)  # Adjust font size
        ax.set_xticks(index)
        ax.set_xticklabels(x_labels, rotation=90, fontsize=8)  # Adjust font size
        ax.legend(fontsize=10)  # Adjust font size

        plt.tight_layout()
        plt.savefig(f'data/plot_action{i}.png')  # Save the plot as a PNG file
        plt.close()  # Close the plot to avoid displaying it in some environments
