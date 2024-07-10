# -*- coding: utf-8 -*-

# Import necessary libraries
import json
import requests
import numpy as np

# Define API_KEY, query, base_url, data, and headers
API_KEY = "4d484b6638b2ca654c8ae49427fd18b8"
query = "NCR18650B"
base_url = 'https://api.elsevier.com/content/search/sciencedirect'

data = {
    "qs": query,
    "date": 2023,
    "volume": 0,
    "display": {
        "show": 10,
        "offset": 0
    }
}

headers = {
    'x-els-apikey': API_KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Function to send request and handle response
def get_response(url, data, headers):
    response = requests.put(url, data=json.dumps(data), headers=headers)
    response = response.text.replace('false', 'False').replace('true', 'True')
    try:
        response = eval(response)
        # print(response)
    except Exception as e:
        print(f"Error evaluating response: {e}")
        response = {}
    return response

# Function to retrieve DOIs
def get_doi(data, volume, year):
    dois = []
    data['volume'] = volume
    data["date"] = year
    response = get_response(base_url, data, headers)
    if 'resultsFound' in response:
        n = int(np.ceil(response['resultsFound'] / 100))
    else:
        n = 60  # Default number of pages to retrieve
    for offset in range(n + 1):
        data["display"]["offset"] = offset
        response = get_response(base_url, data, headers)
        if 'results' in response:
            results = response['results']
            for result in results:
                if 'doi' in result:
                    dois.append(result['doi'])
    return dois

# Function to download articles based on DOI
def download_doi(doi):
    with open(str(doi) + '.xml', 'w', encoding='utf-8') as f:
        request_url = 'https://api.elsevier.com/content/article/doi/{}?apiKey={}&httpAccept=text%2Fxml'.format(
            doi, API_KEY)
        response = requests.get(request_url)
        if response.status_code == 200:
            f.write(response.text)
        else:
            print(f"Failed to download article with DOI {doi}")

# Main script to call get_doi and download articles
if __name__ == "__main__":
    # Example usage:
    volume = 2
    year= 2022
    dois = get_doi(data, volume, year)
    # print("Retrieved DOIs:")
    for doi in dois:
        print(doi)
        download_doi(doi)
