class ExposeScoreBoard:
    def __init__(self, target_url: str):
        self.target_url = target_url

    def run_exploit(self):
        print(f"Executing ExposeScoreBoard on {self.target_url}")
        # Logique pour extraire les données des challenges
        print("[+] Fetching /rest/score-board API...")
        # Exemple : données simulées
        data = {"challenges": [{"id": 1, "name": "Challenge 1", "solved": False}]}
        print(f"[+] Extracted Data: {data}")