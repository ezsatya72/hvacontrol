import pandas as pd
import numpy as np

# Number of records
num_records = 10000

# Generate a timestamp series
timestamps = pd.date_range(start='2022-01-01', periods=num_records, freq='H')

# Chiller data
chiller_cooling_load = np.random.normal(loc=500, scale=50, size=num_records)  # in kW
chiller_power_consumption = chiller_cooling_load * np.random.normal(loc=0.9, scale=0.05, size=num_records)  # in kW

# AHU data
ahu_airflow_rate = chiller_cooling_load * np.random.normal(loc=1.1, scale=0.1, size=num_records)  # in CFM
ahu_temp_diff = np.random.normal(loc=10, scale=1, size=num_records)  # in degrees Celsius
ahu_power_consumption = ahu_airflow_rate * ahu_temp_diff * np.random.normal(loc=0.01, scale=0.005, size=num_records)  # in kW

# Boiler data
boiler_heating_load = ahu_airflow_rate * np.random.normal(loc=0.8, scale=0.1, size=num_records)  # in kW
boiler_fuel_consumption = boiler_heating_load * np.random.normal(loc=0.85, scale=0.05, size=num_records)  # in liters/hour
boiler_power_consumption = boiler_heating_load * np.random.normal(loc=1.1, scale=0.1, size=num_records)  # in kW

# Create dataframes
chiller_data = pd.DataFrame({
    'timestamp': timestamps,
    'cooling_load': chiller_cooling_load,
    'power_consumption': chiller_power_consumption
})

ahu_data = pd.DataFrame({
    'timestamp': timestamps,
    'airflow_rate': ahu_airflow_rate,
    'temperature_difference': ahu_temp_diff,
    'power_consumption': ahu_power_consumption
})

boiler_data = pd.DataFrame({
    'timestamp': timestamps,
    'heating_load': boiler_heating_load,
    'fuel_consumption': boiler_fuel_consumption,
    'power_consumption': boiler_power_consumption
})

# Save to CSV in the specified directory
output_directory = '/home/satya/hvac_mobile/.github/data'

chiller_data.to_csv(f'{output_directory}/chiller_data.csv', index=False)
ahu_data.to_csv(f'{output_directory}/ahu_data.csv', index=False)
boiler_data.to_csv(f'{output_directory}/boiler_data.csv', index=False)

print("CSV files for boilers_data, chiller_data, and ahu_data have been generated.")
