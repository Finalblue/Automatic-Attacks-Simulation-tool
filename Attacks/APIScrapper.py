import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class APIScanner:
    def __init__(self):
        self.api_endpoints = []

    def find_js_endpoints(self, url):
        print("Scraping url ...")
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            js_files = [script['src'] for script in soup.find_all('script') if 'src' in script.attrs]

            endpoints = set()

            for js_file in js_files:
                full_url = urljoin(url, js_file)
                try:
                    js_content = requests.get(full_url, timeout=5).text
                    
                    found_endpoints = re.findall(r'["\'](/[a-zA-Z][^"\']*)["\']', js_content)
                    
                    endpoints.update(found_endpoints)
                except Exception as e:
                    print(f"Error while accessing {full_url}: {str(e)}")
                    continue

            self.api_endpoints = list(endpoints)
            print(f"API endpoints found: {len(endpoints)}")

        except Exception as e:
            print(f"Error while scraping the URL: {e}")

    def get_api_endpoints(self):
        return self.api_endpoints

# if __name__ == "__main__":
    
#     scanner = APIScanner()

#     target_url = "http://45.76.47.218:3000"

#     scanner.find_js_endpoints(target_url)

#     api_endpoints = scanner.get_api_endpoints()
#     for endpoint in api_endpoints:
#         print(endpoint)