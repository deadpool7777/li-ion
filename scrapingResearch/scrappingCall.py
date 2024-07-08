# Import the get_doi function from web-scrap.rsc.py
from scrapingDemoV2 import get_doi, get_response

# Replace with your actual Elsevier API key
API_KEY = "4d484b6638b2ca654c8ae49427fd18b8"
base_url = 'https://api.elsevier.com/content/search/sciencedirect'

headers = {'x-els-apikey': API_KEY,
           'Content-Type': 'application/json',
           'Accept': 'application/json'}

# Example query parameters
query = "NCR18650B"
volume = 2  # Adjust as needed
year = 2020  # Adjust as needed

# Define data dictionary with initial parameters
data = {
    "qs": query,
    "date": year,
    "display": {
        "show": 10,
        "offset": 0
    }
}

# Call get_doi function to retrieve DOIs
dois = get_doi(data, volume, year)

# Print the retrieved DOIs
print("Retrieved DOIs:")
for doi in dois:
    print(doi)

response = get_response(base_url, data, headers)
print("API Response:")
print(response)
