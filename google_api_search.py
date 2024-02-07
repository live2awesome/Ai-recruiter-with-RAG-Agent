import requests

# Define the Google API endpoint and key
GOOGLE_API = 'https://www.googleapis.com/customsearch/v1'
GOOGLE_KEY = 'your-google-api-key'#add google key 

# Search for LinkedIn profiles matching the job criteria
def search_linkedin_profiles(search_parameter, location):
    query = f'{search_parameter} site:linkedin.com/in/ location:"{location}"'
    params = {
        'key': GOOGLE_KEY,
        'cx': 'your-custom-search-engine-id',
        'q': query
    }
    response = requests.get(GOOGLE_API, params=params)
    if response.status_code == 200:
        results = response.json()['items']
        return results
    else:
        return None
