import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class APIScanner:
    def __init__(self):
        self.api_endpoints = []  # Liste pour stocker les endpoints d'API trouvés
    
    def find_js_endpoints(self, url):
        print("Scraping url ...")
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')

            # get all the JS files referenced in the HTML
            js_files = [script['src'] for script in soup.find_all('script') if 'src' in script.attrs]

            #create a list to store unique endpoints
            endpoints = set()

            # Analyze each JS file
            for js_file in js_files:
                full_url = urljoin(url, js_file)  # Créer l'URL complète du fichier JS
                try:
                    # Get JS file content
                    js_content = requests.get(full_url, timeout=5).text
                    # Search for /rest API endpoints
                    found_endpoints = re.findall(r'/rest/[a-zA-Z0-9/._-]+', js_content)
                    endpoints.update(found_endpoints)  # Add enpoints to the list
                except Exception as e:
                    print(f"Error while accessing {full_url}: {str(e)}")
                    continue
            
            self.api_endpoints = list(endpoints)
            print(f"API points : {len(endpoints)}")

        except Exception as e:
            # Gestion des erreurs
            print(f"Error while scrapping the url {e}")

    def get_api_endpoints(self):
        """Return list of endpoints found"""
        return self.api_endpoints

# Exemple

# if __name__ == "__main__":

#     scanner = APIScanner()

#     target_url = "http://45.76.47.218:3000"  # Remplacer par l'URL de votre instance OWASP Juice Shop

#     scanner.find_js_endpoints(target_url)

#     api_endpoints = scanner.get_api_endpoints()
#     for endpoint in api_endpoints:
#         print(endpoint)

