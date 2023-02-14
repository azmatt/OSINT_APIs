import requests
import time

def search_google(query):
    # set up the API endpoint and parameters
    api_key = 'YOUR_API_KEY'
    cx = 'YOUR_CX'

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cx
    }
    
    # make the API request
    response = requests.get(url, params=params).json()
    
    # return the results
    return response.get("items", [])

# list of terms to search for
search_terms = [
    "osint",
    "apis",
    "python",
    # ...
]

# search loop, repeat every 5 minutes
while True:
    for term in search_terms:
        results = search_google(term)
        if results:
            print(f"Results for '{term}':")
            for result in results:
                print(result["title"])
                print(result["link"])
                print()
    time.sleep(300)  # sleep for 5 minutes
