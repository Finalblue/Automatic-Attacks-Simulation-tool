import itertools
import string

def brute_force_password(target_password, max_length=4):
    """
    Essaie de deviner un mot de passe en utilisant la force brute.

    :param target_password: Le mot de passe cible à deviner.
    :param max_length: Longueur maximale du mot de passe.
    :return: Le mot de passe deviné.
    """
    characters = string.ascii_letters + string.digits  # Lettres et chiffres
    for length in range(1, max_length + 1):
        for attempt in itertools.product(characters, repeat=length):
            attempt_password = ''.join(attempt)
            print(f"Trying: {attempt_password}")
            if attempt_password == target_password:
                return attempt_password
    return None
