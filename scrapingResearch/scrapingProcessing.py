import pandas as pd
import re

# Function to extract details
def extract_battery_details(text):
    details = {
        'capacity': None,
        'life': None,
        'weight': None,
        'charge_voltage': None,
        'nominal_voltage': None
    }

    # Extract capacity
    capacity_match = re.search(r'\b(\d+)\s*mAh\b', text, re.IGNORECASE)
    if capacity_match:
        details['capacity'] = capacity_match.group(1) + ' mAh'

    # Extract cycle life
    life_match = re.search(r'\b(\d+)\s*cycles\b', text, re.IGNORECASE)
    if life_match:
        details['life'] = life_match.group(1) + ' cycles'

    # Extract weight
    weight_match = re.search(r'\b(\d+)\s*grams?\b', text, re.IGNORECASE)
    if weight_match:
        details['weight'] = weight_match.group(1) + ' grams'

    # Extract maximum charge voltage
    charge_voltage_match = re.search(r'\b(\d+(\.\d+)?)\s*V\b', text, re.IGNORECASE)
    if charge_voltage_match:
        details['charge_voltage'] = charge_voltage_match.group(1) + ' V'

    # Extract nominal voltage
    nominal_voltage_match = re.search(r'\b(\d+(\.\d+)?)\s*V\b', text, re.IGNORECASE)
    if nominal_voltage_match:
        details['nominal_voltage'] = nominal_voltage_match.group(1) + ' V'

    return details

# Extract details from the example text
# battery_details = extract_battery_details(text)
# battery_details

# Load the CSV file
csv_file_path = './journal_data.csv'
df = pd.read_csv(csv_file_path)

# Function to extract details from a single record
def extract_details_from_record(record):
    paragraphs = ' '.join(record.get('paragraphs', []))
    return extract_battery_details(paragraphs)

# Apply the function to each record
df['details'] = df.apply(extract_details_from_record, axis=1)

# Save the DataFrame to a new CSV file
detailed_csv_file_path = './journal_data_with_details.csv'
df.to_csv(detailed_csv_file_path, index=False)

detailed_csv_file_path
