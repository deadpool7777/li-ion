import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Example: Scraping details
        title = soup.title.text.strip()
        paragraphs = [p.text.strip() for p in soup.find_all('p')]
        links = [a['href'] for a in soup.find_all('a', href=True)]
        
        # Create a dictionary to store scraped data
        data = {
            'title': title,
            'paragraphs': paragraphs,
            'links': links
        }
        
        return data  # Return dictionary directly
    
    else:
        print(f"Failed to retrieve webpage: {response.status_code}")
        return None


def save_data_as_csv(data, filename):
    if isinstance(data, dict):
        # Convert dictionary to a list of dictionaries (one item in the list)
        data = [data]
    
    # Create DataFrame from list of dictionaries
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


# Example usage:
if __name__ == "__main__":
    url = 'https://link.springer.com/article/10.1007/s42452-020-2675-6'  
    scraped_data = scrape_website(url)
    csv_filename = './journal_data.csv'
    
    if scraped_data:
        save_data_as_csv(scraped_data, csv_filename)
        print(f"Data saved to {csv_filename}")
    else:
        print("Scraping failed.")
