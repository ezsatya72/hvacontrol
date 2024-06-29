import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB running on the host machine
client = MongoClient("mongodb://host.docker.internal:27017/")
db = client['hvac']

# Retrieve data from MongoDB collections
boilers_data = pd.DataFrame(list(db['boilers_data_sample'].find()))
chillers_data = pd.DataFrame(list(db['chillers_data'].find()))
ahus_data = pd.DataFrame(list(db['ahus_data_sample'].find()))

# Remove ObjectId columns and any other non-numeric columns
boilers_data = boilers_data.select_dtypes(include=[float, int])
chillers_data = chillers_data.select_dtypes(include=[float, int])
ahus_data = ahus_data.select_dtypes(include=[float, int])

# Display first few rows of each DataFrame
print(boilers_data.head())
print(chillers_data.head())
print(ahus_data.head())

input("Press any key to continue...")
#Perform correlation analysis to identify dependencies between attributes.---------------------------------------------

import seaborn as sns
import matplotlib.pyplot as plt

# Combine data from all collections into a single DataFrame
combined_data = pd.concat([boilers_data, chillers_data, ahus_data], axis=1)

# Calculate correlation matrix
correlation_matrix = combined_data.corr()

# Display correlation matrix
print(correlation_matrix)
input("Press any key to continue...")
# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()


#Based on the correlations, generate recommendations for parameter adjustments.-----------------------------------------

def generate_recommendations(correlation_matrix):
    recommendations = []
    for column in correlation_matrix.columns:
        correlated_features = correlation_matrix[column][correlation_matrix[column].abs() > 0.01].index.tolist()
        correlated_features.remove(column)
        for feature in correlated_features:
            if correlation_matrix.at[column, feature] > 0:
                recommendations.append(f"Increase in {column} is positively correlated with {feature}. Consider adjusting {feature} when {column} increases.")
            else:
                recommendations.append(f"Increase in {column} is negatively correlated with {feature}. Consider adjusting {feature} when {column} decreases.")
    return recommendations

recommendations = generate_recommendations(correlation_matrix)
for recommendation in recommendations:
    print(recommendation)
