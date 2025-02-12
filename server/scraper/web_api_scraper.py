import requests;
from bs4 import BeautifulSoup;

class WebAPIScraper():
  def __init__(self, url : str):
    self.url = url;

  def _isAPIEndPoint(self, url: str) -> bool:
    response = requests.get(url)
    
    # Check if the response is in a JSON format (typical for APIs)
    if response.status_code == 200:
      try:
        # Try parsing the response as JSON
        response.json()
        return True  # The endpoint is likely an API
      except ValueError:
        return False  # Not a JSON response
    return False  # Something went wrong or it's not an API endpoint

  def _fetchPage(self, url : str) -> requests.Response:
    # Include headers because some websites block headerless requests. 
    # This is to mimic a real browser.
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers);

    if (response.status_code != 200):
      print(f"Failed to retrieve webpage. Response code: {response.status_code}");
      return None;
    return response;

  def _extractLinks(self, html : str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser");

    # Find all <a> tags which usually contains hyperlinks;
    links = soup.find_all('a', href=True);
    api_endpoints = [];
    for link in links:
      link_href = link['href'];
      if ('api' in link_href.lower()) or ('endpoint' in link_href.lower()):
        api_endpoints.append(link_href);
    return api_endpoints;

  def _getAllAPIEndpoints(self, home_url : str):
    home_page = self._fetchPage(home_url);
    if home_page:
      api_endpoints = self._extractLinks(home_page.text);

      # Look for pagination links
      soup = BeautifulSoup(home_page.text, "html.parser");
      pagination_links = soup.find_all('a', href=True, text="Next");
      for link in pagination_links:
        next_page_url = link["href"];
        next_page = self._fetchPage(next_page_url);
        if (next_page):
          api_endpoints += self._extractLinks(next_page.text);
      return api_endpoints;


  def scrape(self):
    response = self._fetchPage(self.url);
    if (response == None):
      return;
  
    api_endpoints = self._getAllAPIEndpoints(self.url);

    # Filter out non-api endpoints
    valid_api_endpoints = [];
    for endpoint in api_endpoints:
      if (self._isAPIEndPoint(endpoint)):
        valid_api_endpoints.append(endpoint)

    print(api_endpoints);
    print(valid_api_endpoints);
    return valid_api_endpoints;


