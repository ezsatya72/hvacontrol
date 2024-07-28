import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns

# Replace 'YOUR_WINDOWS_IP' with the actual IP address of your Windows host
client = MongoClient("mongodb://192.168.1.8:27017/")
db = client['hvac']

# Retrieve data from MongoDB collections
boilers_data = pd.DataFrame(list(db['boilers_data'].find()))
chillers_data = pd.DataFrame(list(db['chillers'].find()))
ahus_data = pd.DataFrame(list(db['ahus_data'].find()))

# Remove ObjectId columns and any other non-numeric columns
boilers_data = boilers_data.select_dtypes(include=[float, int])
chillers_data = chillers_data.select_dtypes(include=[float, int])
ahus_data = ahus_data.select_dtypes(include=[float, int])

# Combine data from all collections into a single DataFrame
combined_data = pd.concat([boilers_data, chillers_data, ahus_data], axis=1)

# Check for a timestamp column
time_column = 'timestamp'  # Replace with actual time column name if different

if time_column in combined_data.columns:
    combined_data[time_column] = pd.to_datetime(combined_data[time_column])
else:
    # If there is no timestamp column, create a dummy one for the purpose of plotting
    combined_data['timestamp'] = pd.date_range(start='1/1/2022', periods=len(combined_data), freq='H')

# Line plot
plt.figure(figsize=(12, 8))
for column in combined_data.columns:
    if column != 'timestamp':  # Ensure the column name matches the dummy timestamp
        plt.plot(combined_data['timestamp'], combined_data[column], label=column)
plt.title('Trends Over Time')
plt.xlabel('Time')
plt.ylabel('Values')
plt.legend()
plt.show()

# Calculate correlation matrix
correlation_matrix = combined_data.corr()

# Plot heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)
plt.title('Correlation Heatmap')
plt.show()

# Generate recommendations
def generate_recommendations(correlation_matrix):
    recommendations = []
    for column in correlation_matrix.columns:
        correlated_features = correlation_matrix[column][correlation_matrix[column].abs() > 0.5].index.tolist()
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
