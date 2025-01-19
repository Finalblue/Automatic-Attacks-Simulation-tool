class RetrieveOrders:
    def __init__(self, target_url: str):
        self.target_url = target_url

    def run_exploit(self):
        print(f"Executing RetrieveOrders on {self.target_url}")
        # Logique pour accéder aux commandes d'autres utilisateurs
        print("[+] Fetching /api/Orders API...")
        # Exemple : données simulées
        orders = [{"orderId": 101, "userId": 2, "items": ["item1", "item2"]}]
        print(f"[+] Retrieved Orders: {orders}")
