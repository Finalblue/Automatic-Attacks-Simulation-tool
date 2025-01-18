# AttackManager.py
from typing import Dict, List, Callable
import threading
import asyncio
import subprocess
import sys
import os
from GUI.attack_types import Attack, AttackType

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from Attacks.Alexis.ForgedCoupon import JuiceShopCouponExploit
from Attacks.Alexis.ForgedUnsignedJWT import run_proxy as run_unsigned_proxy
from Attacks.Alexis.ForgedSignedJWT import run_proxy as run_signed_proxy
from Attacks.Alexis.CaptchaBypass import CaptchaBypass
from Attacks.APIScrapper import APIScanner

class AttackManager:
    def __init__(self):
        self._proxy_running = False
        self._mitm_process = None 
        self._attacks = {
            "JuiceShop Coupon": Attack("JuiceShop Coupon", AttackType.DIRECT, self._run_juice_shop),
            "Captcha Bypass": Attack("CaptchaBypass", AttackType.DIRECT, self._run_captcha_bypass),
            "API Scanner": Attack("API Scanner", AttackType.DIRECT, self._run_api_scanner),
            "Unsigned JWT": Attack("Unsigned JWT", AttackType.PROXY, self._run_unsigned_jwt),
            "Signed JWT": Attack("Signed JWT", AttackType.PROXY, self._run_signed_jwt),
            "Launch MITM Proxy": Attack("Launch MITM Proxy", AttackType.PROXY, self._run_mitm_proxy)
        }
        
    @property
    def direct_attacks(self) -> List[str]:
        return [name for name, attack in self._attacks.items() 
                if attack.type == AttackType.DIRECT]

    @property
    def proxy_attacks(self) -> List[str]:
        return [name for name, attack in self._attacks.items() 
                if attack.type == AttackType.PROXY]

    def execute_attack(self, name: str, url: str, use_proxy: bool = False, callback: Callable = None) -> None:
        if name in self._attacks:
            attack = self._attacks[name]
            if attack.type == AttackType.PROXY and not self._proxy_running and name != "Launch MITM Proxy":
                raise ValueError("Proxy must be running for this attack")
            if callback:
                callback(f"Starting {name}...")
            attack.function(url, use_proxy if attack.type == AttackType.DIRECT else True, callback)
            if callback:
                callback(f"Finished {name}")

    def start_proxy(self) -> None:
        self._proxy_running = True

    def stop_proxy(self) -> None:
        self._proxy_running = False

    def _run_juice_shop(self, url: str, use_proxy: bool = False, callback: Callable = None):
        exploit = JuiceShopCouponExploit(url)
        if callback:
            callback("Running coupon exploit...")
        exploit.run_exploit()

    def _run_captcha_bypass(self, url: str, use_proxy: bool = False, callback: Callable = None):
        scanner = CaptchaBypass(url)
        results = scanner.run_all_attacks()
        if callback:
            for name, result in results.items():
                callback(f"{name}: {result['status']}")
                if result['status'] == 'success':
                    callback(f"Details: {result['details']}")

    def _run_api_scanner(self, url: str, use_proxy: bool = False, callback: Callable = None):
        scanner = APIScanner(callback)
        if use_proxy:
            scanner.set_proxy("http://127.0.0.1:8080")
        scanner.find_js_endpoints(url)

    def _run_unsigned_jwt(self, url: str, use_proxy: bool = True, callback: Callable = None):
        if not self._proxy_running:
            raise ValueError("Proxy must be running for JWT attacks")
        if callback:
            callback("Execute the JWT attack through the proxy now")

    def _run_signed_jwt(self, url: str, use_proxy: bool = True, callback: Callable = None):
        if not self._proxy_running:
            raise ValueError("Proxy must be running for JWT attacks") 
        if callback:
            callback("Execute the JWT attack through the proxy now")

    def _run_mitm_proxy(self, url: str, use_proxy: bool = True, callback: Callable = None):
        if self._mitm_process:
            if callback:
                callback("MITM proxy is already running")
            return
            
        if callback:
            callback("Starting MITM proxy...")
        self._mitm_process = subprocess.Popen(
            ["mitmweb", "--mode", "regular", "--listen-port", "8080"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if callback:
            callback("MITM proxy launched on port 8080")

    def stop_proxy(self) -> None:
        if self._mitm_process:
            self._mitm_process.terminate()
            self._mitm_process = None
        self._proxy_running = False