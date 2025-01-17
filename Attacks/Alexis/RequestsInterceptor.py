from mitmproxy import ctx
from mitmproxy.tools.main import mitmdump
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import subprocess
import webbrowser
import sys

JUICE_SHOP_URL = "http://45.76.47.218:3000"
KNOWN_ENDPOINTS = [
    '/rest/memories', '/rest/continue-code/apply/', '/rest/admin',
    '/rest/repeat-notification', '/rest/user/reset-password', '/rest/saveLoginIp',
    '/rest/continue-code-fixIt', '/rest/user/login', '/rest/order-history',
    '/rest/user/whoami', '/rest/continue-code', '/rest/user',
    '/rest/products/search', '/rest/web3', '/rest/deluxe-membership',
    '/rest/admin/application-configuration', '/rest/country-mapping',
    '/rest/languages', '/rest/user/security-question',
    '/rest/continue-code-fixIt/apply/', '/rest/image-captcha/',
    '/rest/continue-code-findIt/apply/', '/rest/user/authentication-details/',
    '/rest/captcha', '/rest/2fa/disable', '/rest/wallet/balance',
    '/rest/2fa/status', '/rest/products', '/rest/chatbot', '/rest/2fa/setup',
    '/rest/continue-code-findIt', '/rest/user/change-password',
    '/rest/2fa/verify', '/rest/basket/', '/rest/track-order'
]

class JuiceShopInterceptor:
    def request(self, flow):
        if JUICE_SHOP_URL in flow.request.pretty_url:
            current_path = flow.request.path
            if any(endpoint in current_path for endpoint in KNOWN_ENDPOINTS):
                print(f"\n[*] Intercepted known endpoint: {current_path}")
                print(f"[*] Method: {flow.request.method}")
                print(f"[*] Headers: {dict(flow.request.headers)}")
                flow.intercept()
            else:
                print(f"\n[!] Unknown endpoint accessed: {current_path}")

def main():
    print("[*] Starting Juice Shop request interceptor...")
    print(f"[*] Monitoring {len(KNOWN_ENDPOINTS)} known endpoints")
    
    # Start mitmweb in a separate process
    cmd = ["mitmweb", "--mode", "regular", "--listen-port", "8080"]
    process = subprocess.Popen(cmd)
    
    # Open browser to web interface
    webbrowser.open("http://127.0.0.1:8081")
    
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()