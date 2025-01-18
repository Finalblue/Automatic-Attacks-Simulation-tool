import requests

class JuiceShopWeirdCryptoExploit:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def fetch_captcha(self):
        endpoint = f"{self.base_url}/rest/captcha"
        print(f"[CAPTCHA] Fetching a captcha...")
        response = self.session.get(endpoint, headers=self.headers)

        if response.status_code == 200:
            captcha_data = response.json()
            captcha_id = captcha_data.get("captchaId")
            captcha_answer = captcha_data.get("answer")  # Récupérer la réponse au CAPTCHA
            print(f"[CAPTCHA] Captcha fetched successfully. ID: {captcha_id}, Answer: {captcha_answer}")
            return captcha_id, captcha_answer
        else:
            print(f"[FAIL] Failed to fetch captcha. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None, None

    def inform_about_weak_crypto(self, captcha_id, captcha_answer):
        endpoint = f"{self.base_url}/api/Feedbacks"
        payload = {
            "comment": "The shop uses MD5 for hashing, which is considered insecure. Please update to a modern algorithm like SHA-256.",
            "rating": 2,
            "captchaId": captcha_id,  # Inclure captchaId
            "captcha": captcha_answer  # Inclure la réponse au CAPTCHA
        }

        print(f"[CRYPTO WARNING] Informing the shop about weak crypto usage...")
        response = self.session.post(endpoint, json=payload, headers=self.headers)

        if response.status_code == 201:  # Code HTTP 201 signifie "Créé"
            print("[SUCCESS] Feedback envoyé avec succès concernant l'utilisation d'algorithmes cryptographiques faibles.")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"[FAIL] Échec de l'envoi du feedback. Statut: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    def run_exploit(self):
        print("[EXPLOIT] Démarrage de l'exploit pour le challenge 'Weird Crypto'...")
        captcha_id, captcha_answer = self.fetch_captcha()
        if not captcha_id or not captcha_answer:
            print("[EXPLOIT] Impossible de récupérer un captcha. Exploit abandonné.")
            return

        success = self.inform_about_weak_crypto(captcha_id, captcha_answer)
        if success:
            print("[EXPLOIT] Exploit terminé avec succès. Flag activé.")
        else:
            print("[EXPLOIT] L'exploit a échoué.")


if __name__ == "__main__":
    base_url = "http://45.76.47.218:3000"  # URL du site Juice Shop
    exploit = JuiceShopWeirdCryptoExploit(base_url)
    exploit.run_exploit()
