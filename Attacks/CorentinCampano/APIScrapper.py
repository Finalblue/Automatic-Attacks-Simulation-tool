import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class APIScrapper:
        
    def __init__(self, callback=None):
        self.callback = callback or print
        self.api_endpoints = []  # Liste pour stocker les endpoints d'API trouvés
        self.session = requests.Session()
        self.session.trust_env = False  # Ignore environment proxies
        self.session.proxies = {'http': None, 'https': None}
    
    def set_proxy(self, proxy_url):
        self.session.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }

    def find_js_endpoints(self, url):
        print("Scraping url ...")
        try:
            response = self.session.get(url, timeout=5, verify=False)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')

            js_files = [script['src'] for script in soup.find_all('script') if 'src' in script.attrs]

            endpoints = set()

            for js_file in js_files:
                full_url = urljoin(url, js_file)
                try:
                    js_content = self.session.get(full_url, timeout=5).text
                    # Search for /rest API endpoints
                    found_endpoints = re.findall(r'["\'](/[a-zA-Z][^"\']*)["\']', js_content)
                    endpoints.update(found_endpoints)  # Add enpoints to the list
                except Exception as e:
                    print(f"Error while accessing {full_url}: {str(e)}")
                    continue

            self.api_endpoints = list(endpoints)
            print(f"API endpoints found: {len(endpoints)}")
            for endpoint in self.api_endpoints:
                self.callback(f"Endpoint found: {endpoint}")


        except Exception as e:
            print(f"Error while scraping the URL: {e}")

    def get_api_endpoints(self):
        return self.api_endpoints
