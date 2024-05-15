import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Load your data
data = pd.read_csv('/home/tadashi_e/Downloads/scored_survey_data.csv')

# Ensure that DisplayType is read correctly
data['DisplayType'] = data['DisplayType'].astype(str).str.strip()  # Remove any trailing spaces
data = data[data['DisplayType'] != 'DisplayType']  # Remove rows where DisplayType is not correctly set

# Convert DisplayType to a categorical variable if it's not already
data['DisplayType'] = data['DisplayType'].astype('category')

# Ensure Q27 is numeric
data['Q43'] = pd.to_numeric(data['Q43'], errors='coerce')

# Drop rows with any missing values in the columns of interest
data = data.dropna(subset=['DisplayType', 'Q43'])

# Check the distribution of DisplayType again
print(data['DisplayType'].value_counts())

# Set up the ANOVA model
model = ols('Q43 ~ C(DisplayType)', data=data).fit()

# Perform the ANOVA
anova_results = sm.stats.anova_lm(model, typ=2)

# Print the ANOVA table
print(anova_results)

