import requests

def fetch_data_from_api(api_url, api_key):
    headers = {
        'Accept': 'application/json',
        # 'Authorization': f'Bearer {auth_token}',
        'X-ELS-APIKey': api_key,
        # 'X-ELS-Insttoken': inst_token,
        # 'X-ELS-ReqId': req_id,
        # 'X-ELS-ResourceVersion': resource_version
    }

    params = {
        'httpAccept': 'application/json',  # This could be a query parameter as per the description
        'apiKey': api_key,  # This could also be a query parameter
        # 'query' :"lI-ion batteries"
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()  # Return JSON data from the response
        else:
            print(f"Error: Status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Example usage
# api_url = "https://api.elsevier.com/content/search/sciencedirect"
api_url = "https://jsonplaceholder.typicode.com/todos/1"
api_key = "98460a4a1d5e4b573f8c0d2cb9df3499"
# auth_token = "your_auth_token_here"
# inst_token = "your_inst_token_here"
# req_id = "6a649563bd2743d3"
# resource_version = "default"  # Example of multiple resource versions

data = fetch_data_from_api(api_url, api_key)
if data:
    print(data)  # Print the entire JSON response
else:
    print("Failed to fetch data from API")
