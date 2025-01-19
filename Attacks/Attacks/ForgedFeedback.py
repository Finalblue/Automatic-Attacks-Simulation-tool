class ForgedFeedback:
    def __init__(self, target_url: str):
        self.target_url = target_url

    def run_exploit(self):
        print(f"Executing ForgedFeedback on {self.target_url}")
        # Logique pour modifier les feedbacks
        payload = {
            "userId": 2,  # Exemple : changer l'ID utilisateur
            "comment": "This is a forged feedback!"
        }
        print(f"[+] Modified Payload: {payload}")
        # Simuler l'envoi de la requête
        print("[+] Sending forged feedback...")
