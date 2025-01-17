import random


def birthday_paradox(num_people, hash_space):
    """
    Simule une collision dans l'espace de hachage basé sur le paradoxe des anniversaires.
    
    :param num_people: Nombre d'individus (ou essais).
    :param hash_space: Taille de l'espace de hachage (ex: 365 pour les jours de l'année).
    :return: Booléen indiquant s'il y a eu collision.
    """
    hashes = set()
    for _ in range(num_people):
        # Générer une valeur "hachée" aléatoire
        hashed_value = random.randint(0, hash_space - 1)
        if hashed_value in hashes:
            return True  # Collision détectée
        hashes.add(hashed_value)
    return False  # Pas de collision


def multiple_trials(num_people, hash_space, trials=10000):
    """
    Simule plusieurs essais pour estimer la probabilité de collision.
    
    :param num_people: Nombre d'individus.
    :param hash_space: Taille de l'espace de hachage.
    :param trials: Nombre de simulations.
    :return: Probabilité estimée d'une collision.
    """
    collisions = sum(birthday_paradox(num_people, hash_space) for _ in range(trials))
    return collisions / trials


hash_space = 365
num_people = 23
trials = 10000

probability = multiple_trials(num_people, hash_space, trials)
print(f"\nPour {num_people} individus dans un espace de hachage de taille {hash_space},")
print(f"la probabilité de collision est d'environ {probability:.2%} sur {trials} essais.\n")
