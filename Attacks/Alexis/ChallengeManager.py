import requests
import logging


class ChallengeManager:
    def __init__(self, base_url):
        self.base_url = base_url
        self.challenges_endpoint = "/rest/challenges"

    def get_challenges(self):
        """Retrieve the status of all challenges."""
        url = self.base_url + self.challenges_endpoint
        try:
            response = requests.get(url)
            if response.status_code == 200:
                challenges = response.json().get("data", [])
                solved_challenges = [
                    {"name": c["name"], "description": c["description"]}
                    for c in challenges if c.get("solved", False)
                ]
                logging.info(f"[+] Retrieved {len(solved_challenges)} solved challenges.")
                return {"status": "success", "solved_challenges": solved_challenges}
            else:
                logging.error("Failed to fetch challenges.")
                return {"status": "failed", "details": response.text}
        except Exception as e:
            logging.error(f"Error fetching challenges: {e}")
            return {"status": "failed", "details": str(e)}
