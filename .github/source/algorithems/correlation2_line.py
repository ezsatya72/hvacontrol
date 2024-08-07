import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns

# Replace 'YOUR_WINDOWS_IP' with the actual IP address of your Windows host
client = MongoClient("mongodb://192.168.1.8:27017/")
db = client['hvac']

# Retrieve data from MongoDB collections
boilers_data = pd.DataFrame(list(db['boiler_data'].find()))
chillers_data = pd.DataFrame(list(db['chiller_data'].find()))
ahus_data = pd.DataFrame(list(db['ahu_data'].find()))

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
    combined_data['timestamp'] = pd.date_range(start='1/1/2022', periods=len(combined_data), freq='h')

# Calculate correlation matrix
correlation_matrix = combined_data.corr()

# Plot heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)
plt.title('Correlation Heatmap')
plt.show()

# Define cooling load and AHU power consumption columns (replace with actual column names if different)
cooling_load_column = 'cooling_load'  # Replace with actual cooling load column name for chillers
ahu_power_column = 'power_consumption'  # Replace with actual power consumption column name for AHUs

# Ensure the specified columns exist in the combined data
if cooling_load_column not in combined_data.columns or ahu_power_column not in combined_data.columns:
    print(f"Columns {cooling_load_column} or {ahu_power_column} not found in the data.")
else:
    # Plot the relationship between cooling load of chiller and power consumption of AHU
    plt.figure(figsize=(12, 8))
    plt.plot(combined_data['timestamp'], combined_data[cooling_load_column], label='Chiller Cooling Load')
    plt.plot(combined_data['timestamp'], combined_data[ahu_power_column], label='AHU Power Consumption')
    plt.title('Relationship between Chiller Cooling Load and AHU Power Consumption')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.legend()
    plt.show()

# Define power consumption columns (replace with actual column names if different)
power_columns = {
    'chiller_data': 'power_consumption',  # Replace with actual chiller power column name
    'ahu_data': 'power_consumption',      # Replace with actual AHU power column name
    'boiler_data': 'power_consumption'    # Replace with actual boiler power column name
}

# Function to plot impact on power consumption
def plot_power_impact(component_data, power_column, component_name):
    if power_column not in component_data.columns:
        print(f"No power consumption data for {component_name}")
        return
    
    critical_params = correlation_matrix[power_column].nlargest(4).index.drop(power_column).tolist()
    
    plt.figure(figsize=(12, 8))
    for param in critical_params:
        plt.plot(combined_data['timestamp'], combined_data[param], label=f'{component_name} - {param}')
    plt.plot(combined_data['timestamp'], combined_data[power_column], label=f'{component_name} - Power Consumption', linewidth=2)
    plt.title(f'Impact on {component_name} Power Consumption')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.legend()
    plt.show()

# Plot impacts for each component
plot_power_impact(chillers_data, power_columns['chiller_data'], 'Chiller')
plot_power_impact(ahus_data, power_columns['ahu_data'], 'AHU')
plot_power_impact(boilers_data, power_columns['boiler_data'], 'Boiler')

# Generate recommendations
def generate_recommendations(correlation_matrix):
    recommendations = []
    for column in correlation_matrix.columns:
        correlated_features = correlation_matrix[column][correlation_matrix[column].abs() > 0.5].index.tolist()
        if column in correlated_features:
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
