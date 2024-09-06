import requests
from bs4 import BeautifulSoup

def fetch_real_time_data(query):
    return generic_search(query)

# Function to handle generic searches
def generic_search(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Fetch the first paragraph of the search result
    result = soup.find('div', class_='BNeawe').text
    if result:
        return result
    else:
        return "No results found."

# Main function to capture and process queries
def main():
    # query = "how many gold medals do india gets in paraolymics'24"
    query = "what is the current time in usa"

    # Fetch real-time data based on the query
    response = fetch_real_time_data(query)
    print(response)

if __name__ == "__main__":
    main()
