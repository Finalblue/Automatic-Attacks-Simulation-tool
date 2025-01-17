import requests
import logging
from bs4 import BeautifulSoup


class Spider:
    def __init__(self, base_url):
        self.base_url = self.validate_url(base_url)
        self.visited_urls = set()
        self.endpoints = []
        self.ajax_endpoints = []

    @staticmethod
    def validate_url(url):
        """Ensure the URL starts with http or https."""
        if not url.startswith("http://") and not url.startswith("https://"):
            return "http://" + url
        return url

    def crawl(self, depth=3):
        """Discover all endpoints via spidering with configurable depth."""
        queue = [(self.base_url, 0)]
        while queue:
            current_url, current_depth = queue.pop(0)
            if current_url in self.visited_urls or current_depth > depth:
                continue

            try:
                response = requests.get(current_url, timeout=5)
                if response.status_code == 200:
                    self.visited_urls.add(current_url)
                    soup = BeautifulSoup(response.text, "html.parser")
                    for link in soup.find_all("a", href=True):
                        full_url = requests.compat.urljoin(self.base_url, link["href"])
                        if full_url not in self.visited_urls and full_url.startswith(self.base_url):
                            self.endpoints.append(full_url)
                            queue.append((full_url, current_depth + 1))
            except Exception as e:
                logging.warning(f"Error crawling {current_url}: {e}")

        return self.endpoints

    def ajax_spider(self):
        """Detect AJAX endpoints by inspecting JS and responses."""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                scripts = soup.find_all("script")
                for script in scripts:
                    if script.string:
                        # Look for patterns "/api/" in JavaScript code
                        self.ajax_endpoints.extend(
                            [line for line in script.string.split() if "/api/" in line]
                        )
            # Inspect JavaScript files discovered during crawling
            for endpoint in self.endpoints:
                if endpoint.endswith(".js"):
                    try:
                        js_response = requests.get(endpoint, timeout=5)
                        if js_response.status_code == 200:
                            self.ajax_endpoints.extend(
                                [line for line in js_response.text.split() if "/api/" in line]
                            )
                    except Exception as e:
                        logging.warning(f"Error accessing JS file {endpoint}: {e}")
        except Exception as e:
            logging.warning(f"Error inspecting AJAX requests: {e}")

        return list(set(self.ajax_endpoints))
