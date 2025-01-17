import requests
from bs4 import BeautifulSoup
import logging


class EndpointDiscoverer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_urls = set()
        self.discovered_endpoints = []

    def spider(self):
        """Basic spider to crawl all accessible URLs."""
        queue = [self.base_url]
        while queue:
            current_url = queue.pop(0)
            if current_url in self.visited_urls:
                continue

            self.visited_urls.add(current_url)
            try:
                response = requests.get(current_url, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    for link in soup.find_all("a", href=True):
                        full_url = requests.compat.urljoin(self.base_url, link["href"])
                        if full_url not in self.visited_urls and full_url.startswith(self.base_url):
                            queue.append(full_url)
                            self.discovered_endpoints.append(full_url)
            except Exception as e:
                logging.warning(f"Error accessing {current_url}: {e}")

        return self.discovered_endpoints

    def ajax_spider(self):
        """Detect AJAX endpoints by inspecting XHR requests."""
        ajax_endpoints = []
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                scripts = soup.find_all("script")
                for script in scripts:
                    if script.string:
                        # Heuristic: Look for AJAX endpoints in JS
                        if "/api/" in script.string:
                            ajax_endpoints.extend(
                                [line for line in script.string.split() if "/api/" in line]
                            )
        except Exception as e:
            logging.warning(f"Error inspecting AJAX requests: {e}")

        self.discovered_endpoints.extend(ajax_endpoints)
        return list(set(self.discovered_endpoints))
