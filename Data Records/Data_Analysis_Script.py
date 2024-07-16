import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi

# Sample data for illustration purposes
data = {
    'Visual_Display_Type': ['Animated Eyes', 'Static Eyes', 'Icons'] * 5,
    'Perceived_Usefulness': [7, 6, 5, 8, 7, 5, 6, 5, 4, 7, 8, 6, 5, 5, 7],
    'Understandability': [8, 7, 6, 9, 8, 6, 7, 6, 5, 8, 9, 7, 6, 6, 8],
    'Predictability': [7, 6, 5, 8, 7, 5, 6, 5, 4, 7, 8, 6, 5, 5, 7],
    'Trust': [8, 7, 6, 9, 8, 6, 7, 6, 5, 8, 9, 7, 6, 6, 8],
    'Likability': [9, 8, 7, 10, 9, 7, 8, 7, 6, 9, 10, 8, 7, 7, 9],
    'Response_Time': [2.5, 3.0, 3.5, 2.0, 2.5, 3.5, 3.0, 3.5, 4.0, 2.5, 2.0, 3.0, 3.5, 3.5, 2.5],
    'Success_Rate': [0.9, 0.8, 0.7, 0.95, 0.9, 0.75, 0.8, 0.7, 0.6, 0.85, 0.95, 0.8, 0.75, 0.8, 0.85],
    'Total_Commands': [15, 20, 18, 14, 15, 21, 19, 18, 22, 16, 14, 20, 18, 18, 15]
}

df = pd.DataFrame(data)

# Plotting average survey ratings by visual display type
mean_ratings = df.groupby('Visual_Display_Type').mean()

# Bar chart for average ratings
mean_ratings[['Perceived_Usefulness', 'Understandability', 'Predictability', 'Trust', 'Likability']].plot(kind='bar', figsize=(10, 6))
plt.title('Average Survey Ratings by Visual Display Type')
plt.ylabel('Average Rating')
plt.xlabel('Visual Display Type')
plt.legend(title='Survey Questions')
plt.show()

# Box plot for distribution of survey ratings
melted_df = df.melt(id_vars=['Visual_Display_Type'], value_vars=['Perceived_Usefulness', 'Understandability', 'Predictability', 'Trust', 'Likability'], var_name='Question', value_name='Rating')

plt.figure(figsize=(12, 6))
sns.boxplot(x='Question', y='Rating', hue='Visual_Display_Type', data=melted_df)
plt.title('Distribution of Survey Ratings by Visual Display Type')
plt.ylabel('Rating')
plt.xlabel('Survey Question')
plt.legend(title='Visual Display Type')
plt.show()

# Heatmap for correlation matrix
correlation_matrix = df[['Perceived_Usefulness', 'Understandability', 'Predictability', 'Trust', 'Likability', 'Response_Time', 'Success_Rate', 'Total_Commands']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Survey Ratings and Performance Metrics')
plt.show()

# Radar chart for survey ratings
def create_radar_chart(df, categories, title):
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    for index, row in df.iterrows():
        values = row[categories].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=row['Visual_Display_Type'])
        ax.fill(angles, values, alpha=0.1)
    
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    plt.title(title)
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    plt.show()

create_radar_chart(mean_ratings.reset_index(), ['Perceived_Usefulness', 'Understandability', 'Predictability', 'Trust', 'Likability'], 'Survey Ratings Radar Chart')

# Scatter plot for response time vs. perceived usefulness
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Perceived_Usefulness', y='Response_Time', hue='Visual_Display_Type', data=df)
plt.title('Response Time vs. Perceived Usefulness by Visual Display Type')
plt.xlabel('Perceived Usefulness')
plt.ylabel('Response Time (seconds)')
plt.legend(title='Visual Display Type')
plt.show()

# Scatter plot for success rate vs. trust
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Trust', y='Success_Rate', hue='Visual_Display_Type', data=df)
plt.title('Success Rate vs. Trust by Visual Display Type')
plt.xlabel('Trust')
plt.ylabel('Success Rate')
plt.legend(title='Visual Display Type')
plt.show()