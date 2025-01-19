import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import json
import os
from typing import Set, List
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

MAX_DEPTH = 3

class SiteExplorer:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.discovered_urls = set()
        self.visited_urls = set()
        self.interesting_urls = set()
        self.setup_selenium()
        
    def setup_selenium(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        
    def extract_links(self, text: str, url: str) -> None:
        patterns = [
            r'[\'\"](/[a-zA-Z0-9_\-./]+\.[a-zA-Z0-9]+)[\'"]',  
            r'href=[\'"]([^"\']+)[\'"]',
            r'(?<=[\'"/])(/[a-zA-Z0-9_\-./]+)(?=[\'"])',
            r'url\([\'"]?([^\'"\)]+)[\'"]?\)',
            r'src=[\'"]([^"\']+)[\'"]',
            r'path:\s*[\'"]([^"\']+)[\'"]',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                path = match.group(1)
                if path.startswith(('javascript:', '#', 'data:', 'mailto:', 'tel:')):
                    continue
                full_url = urljoin(url, path)
                if self.is_internal_url(full_url):
                    self.discovered_urls.add(full_url)
                    if self.is_interesting_url(full_url):
                        self.interesting_urls.add(full_url)
                    
    def crawl_page(self, url: str, depth: int = 0, max_depth: int = MAX_DEPTH) -> None:
        if depth > max_depth or url in self.visited_urls:
            return
            
        self.visited_urls.add(url)
        print(f"[*] Crawling: {url}")
        
        try:
            self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            for tag in soup.find_all(['a', 'link', 'script', 'img', 'form'], href=True) + \
                       soup.find_all(['a', 'link', 'script', 'img', 'form'], src=True):
                for attr in ['href', 'src', 'action']:
                    if tag.has_attr(attr):
                        link = tag[attr]
                        full_url = urljoin(url, link)
                        if self.is_internal_url(full_url):
                            self.discovered_urls.add(full_url)
                            if self.is_interesting_url(full_url):
                                self.interesting_urls.add(full_url)
            
            self.extract_links(self.driver.page_source, url)
            
            new_links = {link for link in self.discovered_urls 
                        if link not in self.visited_urls 
                        and self.is_internal_url(link)}
                        
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(lambda link: self.crawl_page(link, depth + 1, max_depth), 
                           new_links)

        except Exception as e:
            print(f"[!] Error crawling {url}: {e}")

    def is_internal_url(self, url: str) -> bool:
        try:
            return urlparse(self.base_url).netloc == urlparse(url).netloc
        except:
            return False

    def is_interesting_url(self, url: str) -> bool:
        interesting_patterns = [
            r'/api/',r'/admin',r'/upload',r'/files?/',r'/backup',r'/config',r'\.(?:md|sql|env|ini|conf|json|yml|xml)$',
            r'/login',r'/auth',r'/user',r'/private',r'/dev',r'/test',r'/ftp',r'/docs?/',r'/debug',r'\.(?:log|bak|old|tmp)$'
        ]
        url_lower = url.lower()
        return any(re.search(pattern, url_lower) for pattern in interesting_patterns)

    def cleanup_url(self, url: str) -> str:
        return re.sub(r'\?.*$', '', re.sub(r'#.*$', '', url))

    def save_interesting_urls(self) -> None:
        if not os.path.exists('files'):
            os.makedirs('files')
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'files/interesting_urls_{timestamp}.json'
        
        data = {
            'base_url': self.base_url,
            'crawl_depth': MAX_DEPTH,
            'scan_date': datetime.now().isoformat(),
            'interesting_urls': sorted(list(self.interesting_urls))
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\n[+] Interesting URLs saved to: {filename}")

    def run(self) -> None:
        try:
            self.crawl_page(self.base_url)
        finally:
            self.driver.quit()

        print("\n[+] All URLs:")
        for url in sorted(self.discovered_urls):
            print(f"  {url}")

        print("\n[+] Potentially interesting URLs:")
        for url in sorted(self.interesting_urls):
            print(f"  {url}")
            
        self.save_interesting_urls()

if __name__ == "__main__":
    base_url = "http://45.76.47.218:3000"
    explorer = SiteExplorer(base_url)
    explorer.run()