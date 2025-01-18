from mitmproxy import ctx
from mitmproxy.tools.main import mitmdump
import subprocess
import webbrowser
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from APIScrapper import APIScrapper

class JuiceShopInterceptor:
    def __init__(self):
        # Get endpoints dynamically using APIScrapper
        scanner = APIScrapper()
        scanner.find_js_endpoints("http://45.76.47.218:3000")
        self.endpoints = scanner.get_api_endpoints()
        print(f"[*] Loaded {len(self.endpoints)} endpoints")

    def request(self, flow):
        if "45.76.47.218:3000" in flow.request.pretty_url:
            current_path = flow.request.path
            if any(endpoint in current_path for endpoint in self.endpoints):
                print(f"\n[*] Intercepted endpoint: {current_path}")
                print(f"[*] Method: {flow.request.method}")
                print(f"[*] Headers: {dict(flow.request.headers)}")
                flow.intercept()
            else:
                print(f"\n[!] Unknown endpoint: {current_path}")

def requestIntercept():
    print("[*] Starting interceptor with dynamic API scanning...")
    cmd = ["mitmweb", "--mode", "regular", "--listen-port", "8080"]
    process = subprocess.Popen(cmd)
    
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()

# def main():
#     print("[*] Starting interceptor with dynamic API scanning...")
#     cmd = ["mitmweb", "--mode", "regular", "--listen-port", "8080"]
#     process = subprocess.Popen(cmd)
    
#     try:
#         process.wait()
#     except KeyboardInterrupt:
#         process.terminate()

# if __name__ == "__main__":
#     main()