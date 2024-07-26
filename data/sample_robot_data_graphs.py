# import numpy as np
# import matplotlib.pyplot as plt

# # Setting the seed for reproducibility
# np.random.seed(0)

# # Define the groups and metrics
# groups = ['Static Icons', 'Static Eyes', 'Animated Eyes']
# metrics = ['Times Robot Hit Wall', 'Steps Taken', 'Commands Given', 'Inconsistencies', 'Times Robot Hit Wall Again']

# # Generate random sample data according to the constraints mentioned
# data = {
#     'Static Icons': [
#         np.random.randint(1, 5, size=10),  # Times Robot Hit Wall
#         np.random.randint(100, 200, size=10),  # Steps Taken
#         np.random.randint(50, 100, size=10),  # Commands Given
#         np.random.randint(10, 50, size=10),  # Inconsistencies
#         np.random.randint(1, 5, size=10)  # Times Robot Hit Wall Again
#     ],
#     'Static Eyes': [
#         np.random.randint(0, 4, size=10),
#         np.random.randint(150, 250, size=10),
#         np.random.randint(75, 150, size=10),
#         np.random.randint(20, 75, size=10),
#         np.random.randint(0, 4, size=10)
#     ],
#     'Animated Eyes': [
#         np.random.randint(2, 6, size=10),
#         np.random.randint(200, 300, size=10),
#         np.random.randint(100, 200, size=10),
#         np.random.randint(30, 100, size=10),
#         np.random.randint(2, 6, size=10)
#     ]
# }

# # Adjust Commands Given to not exceed Steps Taken or Inconsistencies
# for group in data.values():
#     group[2] = np.minimum(group[2], np.minimum(group[1], group[3]))

# # Plotting
# fig, ax = plt.subplots(figsize=(15, 8))
# width = 0.15  # the width of the bars
# x = np.arange(len(metrics))  # the label locations

# for i, group in enumerate(groups):
#     means = [np.mean(data[group][j]) for j in range(len(metrics))]
#     stds = [np.std(data[group][j]) for j in range(len(metrics))]
#     # Position the bars closer to each other within the same group
#     bar_positions = x - width + i * (width / (len(groups) - 1)) * 2
#     ax.bar(bar_positions, means, width/len(groups), yerr=stds, label=group, capsize=5)

# # Labeling and aesthetics
# ax.set_xlabel('Metrics')
# ax.set_ylabel('Values')
# ax.set_title('Group Comparative Metrics Across Conditions')
# ax.set_xticks(x)
# ax.set_xticklabels(metrics)
# ax.legend(title='Groups')

# plt.show()



# import numpy as np
# import matplotlib.pyplot as plt

# # Generating sample data
# np.random.seed(0)
# time = np.arange(0, 300, 10)  # Time from 0 to 300 seconds in 10-second increments
# groups = ['Static Icons', 'Static Eyes', 'Animated Eyes']

# # Generate data for each group
# # Static Icons - no correlation, random fluctuations
# static_icons = np.random.normal(30, 10, size=len(time))

# # Static Eyes - slight correlation
# static_eyes = time * 0.05 + np.random.normal(0, 5, size=len(time))

# # Animated Eyes - stronger correlation
# animated_eyes = time * 0.1 + np.random.normal(0, 3, size=len(time))

# # Packing data into a dictionary for easier plotting
# data = {
#     'Static Icons': static_icons,
#     'Static Eyes': static_eyes,
#     'Animated Eyes': animated_eyes
# }

# # Creating line plots
# fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
# fig.suptitle('Time Difference Between Robot Display and Command Given')

# for ax, (group, values) in zip(axes, data.items()):
#     ax.plot(time, values, label=f'{group}', marker='o')
#     ax.set_title(group)
#     ax.set_xlabel('Time Elapsed (s)')
#     ax.grid(True)

# axes[0].set_ylabel('Time Difference (s)')
# plt.legend()
# plt.tight_layout()
# plt.show()
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Define the groups and metrics
groups = ['Icons', 'Static Eyes', 'Animated Eyes']
metrics = ['Trust', 'Understandability', 'Perceived Success']

# Generate random sample data for each group and metric
data = {
    'Icons': np.random.randint(1, 8, size=3),
    'Static Eyes': np.random.randint(1, 8, size=3),
    'Animated Eyes': np.random.randint(1, 8, size=3)
}

# Create a radar chart
labels = np.array(metrics)
num_vars = len(labels)

# Compute angle for each axis
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]  # Complete the loop

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
fig.suptitle('Survey Ratings Radar Chart for Display Types')

# Draw one axe per variable and add labels
plt.xticks(angles[:-1], labels, color='grey', size=12)

# Draw ylabels
ax.set_rlabel_position(30)
plt.yticks([1, 3, 5, 7], ["1", "3", "5", "7"], color="grey", size=7)
plt.ylim(0, 7)

# Plot each group
for group, values in data.items():
    values = np.concatenate((values, [values[0]]))  # Repeat the first value to close the circle
    ax.plot(angles, values, linewidth=1, linestyle='solid', label=group)
    ax.fill(angles, values, alpha=0.25)

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.show()


# import numpy as np
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Assume random data for all metrics across the three groups: Icons, Static Eyes, Animated Eyes
# np.random.seed(0)
# # Metrics include both qualitative and quantitative data points
# columns = ['Times Robot Hit Wall', 'Steps Taken', 'Commands Given', 'Inconsistencies', 
#            'Trust', 'Perceived Success', 'Understandability']

# # Generate sample data (as if aggregated into means or medians for each group)
# data_icons = np.random.rand(7)
# data_static_eyes = np.random.rand(7)
# data_animated_eyes = np.random.rand(7)

# # Combine into a DataFrame
# df = pd.DataFrame([data_icons, data_static_eyes, data_animated_eyes], columns=columns)
# df.index = ['Icons', 'Static Eyes', 'Animated Eyes']

# # Calculate the correlation matrix
# corr = df.T.corr()  # Transpose to get correlations between groups, not metrics

# # Creating a heatmap for the correlation matrix
# plt.figure(figsize=(10, 8))
# sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", xticklabels=df.index, yticklabels=df.index)
# plt.title('Correlation Matrix Across Display Types')
# plt.show()
