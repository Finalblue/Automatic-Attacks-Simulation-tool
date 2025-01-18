from typing import Dict, List
import threading
import asyncio
from ForgedCoupon import JuiceShopCouponExploit
from Attacks.Alexis.ForgedUnsignedJWT import run_proxy as run_unsigned_proxy
from Attacks.Alexis.ForgedSignedJWT import run_proxy as run_signed_proxy
from Attacks.Alexis.JuiceShopVulnerabilities import JuiceShopVulnerabilities
from Attacks.Alexis.RequestsInterceptor import JuiceShopInterceptor
import subprocess

class AttackManager:
    def __init__(self):
        self._proxy_thread = None
        self._attacks = {
            "JuiceShop Coupon": self._run_juice_shop,
            "Unsigned JWT": self._run_unsigned_jwt,
            "Signed JWT": self._run_signed_jwt,
            "Vulnerability Scanner": self._run_vulnerability_scan,
            "Dynamic API Interceptor": self._run_api_interceptor
        }
        self._execution_order = ["JuiceShop Coupon", "Unsigned JWT", "Signed JWT", "Vulnerability Scanner", "Dynamic API Interceptor"]

    def _run_juice_shop(self, url: str):
        exploit = JuiceShopCouponExploit(url)
        exploit.run_exploit()

    def _run_unsigned_jwt(self, url: str):
        self._run_proxy(run_unsigned_proxy)

    def _run_signed_jwt(self, url: str):
        self._run_proxy(run_signed_proxy)

    def _run_proxy(self, proxy_func):
        def run_proxy_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(proxy_func())
            except KeyboardInterrupt:
                print("Proxy stopped")
            finally:
                loop.close()

        if self._proxy_thread and self._proxy_thread.is_alive():
            print("Proxy already running")
            return

        self._proxy_thread = threading.Thread(target=run_proxy_thread)
        self._proxy_thread.daemon = True
        self._proxy_thread.start()
        print("Proxy started on 127.0.0.1:8080")

    def _run_vulnerability_scan(self, url: str):
        scanner = JuiceShopVulnerabilities(url)
        results = scanner.run_all_attacks()
        for name, result in results.items():
            print(f"\n{name}: {result['status']}")
            if result['status'] == 'success':
                print(f"Details: {result['details']}")

    def _run_api_interceptor(self, url: str):
        subprocess.Popen(["mitmweb", "--mode", "regular", "--listen-port", "8080"])
        
    @property
    def attack_names(self) -> List[str]:
        return self._execution_order

    def execute_attack(self, name: str, url: str) -> None:
        if name in self._attacks:
            self._attacks[name](url)

    def execute_all(self, url: str) -> None:
        for name in self._execution_order:
            print(f"Executing attack: {name}")
            self.execute_attack(name, url)