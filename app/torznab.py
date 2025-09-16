import requests
import xml.etree.ElementTree as ET

def search(indexer_url, api_key, query):
    """
    Searches a Torznab indexer for a given query.
    """
    params = {
        't': 'search',
        'q': query,
        'cat': '7020',  # E-books category, a common one for books
        'apikey': api_key
    }

    try:
        response = requests.get(indexer_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to indexer: {e}")
        return []

    results = []
    try:
        root = ET.fromstring(response.content)
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            # You can extract more info here, e.g., size, pubDate
            results.append({'title': title, 'link': link})
    except ET.ParseError as e:
        print(f"Error parsing XML response: {e}")
        return []

    return results
