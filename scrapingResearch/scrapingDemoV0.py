import re
import json
import pandas as pd

# Define a function to clean and parse the text data
def clean_and_parse_text(raw_text):
    sections = {
        "title": "",
        "battery modeling results and discussion": "",
        "conclusion and perspectives": ""
    }
    
    # Patterns to match the sections
    patterns = {
        "battery modeling results and discussion": r'battery modeling results and discussion:(.*?)(?:conclusion and perspectives|$)',
        "conclusion and perspectives": r'conclusion and perspectives:(.*?)(?:References|$)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, raw_text, re.DOTALL | re.IGNORECASE)
        if match:
            sections[key] = match.group(1).strip()
    
    return sections

# Function to read data from a CSV file and parse each row
def process_csv(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Initialize a list to hold parsed data
    parsed_data_list = []
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        raw_text = row['body']  # Assuming the CSV file has a column named 'body'
        parsed_data = clean_and_parse_text(raw_text)
        parsed_data['title'] = row['title']  # Include the title in the parsed data
        parsed_data_list.append(parsed_data)
    
    return parsed_data_list

# Path to the input CSV file
csv_file_path = './journal_data.csv'

# Process the CSV file and parse the text data
parsed_data_list = process_csv(csv_file_path)

# Save the parsed data to JSON and CSV formats
# Save to JSON
with open('./parsed_battery_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(parsed_data_list, json_file, ensure_ascii=False, indent=4)

# Save to CSV
parsed_df = pd.DataFrame(parsed_data_list)
parsed_df.to_csv('./parsed_battery_data.csv', index=False)

print("Data has been saved in JSON and CSV formats.")
