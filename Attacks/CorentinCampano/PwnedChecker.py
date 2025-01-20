import requests
import hashlib
import json


class PwnedChecker:
    
    def __init__(self, callback=None):
        self.api_url = "https://haveibeenpwned.com/api/v3"
        self.headers = {
            "User-Agent": "PwnedCheckerScript"
        }
        self.callback = callback or print

    
    def check_email(self, email):
        url = f"{self.api_url}/breachedaccount/{email}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                breaches = response.json()
                self.callback(f"[+] {email} found in {len(breaches)} breach(es):")
                for breach in breaches:
                    self.callback(f"  - {breach['Name']}: {breach['BreachDate']}")
            elif response.status_code == 404:
                self.callback(f"[-] {email} not found in any breaches.")
            else:
                self.callback(f"[!] Error checking {email}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.callback(f"Error checking {email}: {e}")

    def check_password(self, password):
        hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = hashed_password[:5], hashed_password[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Recherche du suffixe dans la réponse
                hashes = response.text.splitlines()
                for hash_entry in hashes:
                    hash, count = hash_entry.split(":")
                    if hash == suffix:
                        print(f"[+] Password '{password}' found in {count} breach(es).")
                        return
                self.callback(f"[-] Password '{password}' not found in any breaches.")
            else:
                self.callback(f"[!] Error checking password: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.callback(f"Error checking password: {e}")

# Exemple d'utilisation
# if __name__ == "__main__":
#     checker = PwnedChecker()

#     target_url = "http://45.76.47.218:3000"  # Replace with your target URL

#     # Create an instance of the APIScanner class to find API endpoints
#     scanner = APIScanner()
#     scanner.find_js_endpoints(target_url)

#     # Get the API endpoints found
#     api_endpoints = scanner.get_api_endpoints()

#     tester = APITester()
#     # Test all found API endpoints
#     for endpoint in api_endpoints:
#         tester.test_endpoint(target_url + endpoint)

#     # Print credentials
#     credentials = tester.get_credentials()

#     for email, password in credentials.items():
#         # Vérification de l'email
#         checker.check_email(email)
        
#         # Vérification du mot de passe
#         checker.check_password(password)
