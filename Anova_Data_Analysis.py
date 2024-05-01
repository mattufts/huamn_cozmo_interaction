import pandas as pd
from scipy.stats import f_oneway

# Read the CSV file
csv_file = 'Robot Guidance Survey_April 30, 2024_09.41.csv'
data = pd.read_csv(csv_file)

# Perform ANOVA comparison
anova_results = f_oneway(data['response1'], data['response2'], data['response3'])

# Print the ANOVA results
print('ANOVA Results:')
print('F-value:', anova_results.statistic)
print('p-value:', anova_results.pvalue)