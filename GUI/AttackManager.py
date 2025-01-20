import threading
from typing import Dict, List, Callable
from Attacks.Alexis.ForgedSignedJWT import signedJWT
from Attacks.Alexis.ForgedUnsignedJWT import unsignedJWT
from Attacks.CorentinCampano.ddos import start_ddos
from GUI.attack_types import Attack, AttackType
from Attacks.Alexis.ForgedCoupon import JuiceShopCouponExploit
from Attacks.Alexis.CaptchaBypass import CaptchaBypass
from Attacks.CorentinCampano.APIScrapper import APIScrapper
from Attacks.CorentinCampano.APITest import APITester
from Attacks.CorentinCampano.PwnedChecker import PwnedChecker
from Attacks.Alexis.RequestsInterceptor import requestIntercept
from Attacks.Maxence.UserCredentials import UserCredentials
from Attacks.Maxence.TFA import TFA
from Attacks.sql_injection import simulate_sql_injection
from Attacks.XXE import exploit_xxe
from Attacks.reflected_xss import simulate_reflected_xss
from Attacks.AdminRegistration import AdminRegistration
from Attacks.WeirdCrypto import WeirdCrypto
from Attacks.EmptyUserRegistration import EmptyUserRegistration

class AttackManager:
    def __init__(self):
        self._proxy_running = False
        self._proxy_thread = None
        self._stop_event = threading.Event()
        self._attacks = {
            "JuiceShop Coupon": Attack("JuiceShop Coupon", AttackType.DIRECT, self._run_forged_coupon),
            "Captcha Bypass": Attack("CaptchaBypass", AttackType.DIRECT, self._run_captcha_bypass),
            "API Scanner": Attack("API Scanner", AttackType.DIRECT, self._run_api_scanner),
            "API Tester": Attack("API Tester", AttackType.DIRECT, self._run_api_tester),
            "DDOS": Attack("DDOS", AttackType.DIRECT, self._run_DDOS),
            "Unsigned JWT": Attack("Unsigned JWT", AttackType.PROXY, self._run_unsigned_jwt),
            "Signed JWT": Attack("Signed JWT", AttackType.PROXY, self._run_signed_jwt),
            "Intercept Requests": Attack("Intercept Requests", AttackType.PROXY, self._run_request_intercept),
            "User Credentials": Attack("User Credentials", AttackType.DIRECT, self._run_user_credentials),
            "Two Factor Authentificator": Attack("Two Factor Authentificator", AttackType.DIRECT, self._run_two_factor_authentificator),
            "SQL Injection": Attack("SQL Injection", AttackType.DIRECT, self._run_sql_injection),
            "XXE": Attack("XXE", AttackType.DIRECT, self._run_xxe_data),
            "XSS": Attack("XSS", AttackType.DIRECT, self. _run_xss),
            "Admin Registration": Attack("Admin Registration", AttackType.DIRECT, self._run_admin_registration),
            "Weird Crypto": Attack("Weird Crypto", AttackType.DIRECT, self._run_weird_crypto),
            "Empty User Registration": Attack("Empty User Registration", AttackType.DIRECT, self._run_empty_user_registration),
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
        """
        Executes a specific attack based on the name provided.
        """
        if name not in self._attacks:
            if callback:
                callback(f"Attack '{name}' not found.")
            return
        
        attack = self._attacks[name]
        if attack.type == AttackType.PROXY and not self._proxy_running:
            if callback:
                callback("Starting proxy for proxy-dependent attack...")
            self.start_proxy(callback)
        if callback:
            callback(f"Starting {name}...")
        attack.function(url, use_proxy if attack.type == AttackType.DIRECT else True, callback)
        if callback:
            callback(f"Finished {name}")

    def start_proxy(self, callback: Callable = None) -> None:
        """
        Starts the proxy in a separate thread to avoid blocking the program.
        """
        if self._proxy_running:
            if callback:
                callback("Proxy is already running.")
            return
        
        if callback:
            callback("Launching proxy...")
        self._stop_event.clear()
        self._proxy_thread = threading.Thread(target=self._run_proxy, args=(callback,))
        self._proxy_thread.start()
        self._proxy_running = True

    def stop_proxy(self, callback: Callable = None) -> None:
        """
        Stops the proxy gracefully.
        """
        if not self._proxy_running:
            if callback:
                callback("Proxy is not running.")
            return

        if callback:
            callback("Stopping proxy...")
        self._stop_event.set()
        self._proxy_thread.join()
        self._proxy_running = False
        if callback:
            callback("Proxy stopped.")

    def _run_proxy(self, callback: Callable = None) -> None:
        """
        Proxy runner function executed in a separate thread.
        """
        try:
            requestIntercept()
        except Exception as e:
            if callback:
                callback(f"Error in proxy: {e}")

    def _run_forged_coupon(self, url: str, use_proxy: bool = False, callback: Callable = None):
        exploit = JuiceShopCouponExploit(url, callback=callback)
        if callback:
            callback("Running coupon exploit...")
        exploit.run_exploit()

    def _run_captcha_bypass(self, url: str, use_proxy: bool = False, callback: Callable = None):
        """
        Executes the Captcha Bypass attack.
        """
        scanner = CaptchaBypass(url)
        results = scanner.run_all_attacks()
        if callback:
            for name, result in results.items():
                callback(f"{name}: {result['status']}")
                if result['status'] == 'success':
                    callback(f"Details: {result['details']}")

    def _run_api_scanner(self, url: str, use_proxy: bool = False, callback: Callable = None):
        """
        Executes the API Scanner.
        """
        scanner = APIScrapper(callback)
        if use_proxy:
            scanner.set_proxy("http://127.0.0.1:8080")
        scanner.find_js_endpoints(url)

    def _run_api_tester(self, url: str, use_proxy: bool = False, callback: Callable = None):
        """
        Executes the API Tester.
        """
        scanner = APIScrapper(callback)
        if use_proxy:
            scanner.set_proxy("http://127.0.0.1:8080")
        scanner.find_js_endpoints(url)
        api_endpoints = scanner.get_api_endpoints()
        tester = APITester(callback)
        for endpoint in api_endpoints:
            tester.test_endpoint(url + endpoint)
        credentials = tester.get_credentials()
        callback("Exposed credentials found:")
        for email, password in credentials.items():
            callback(f"  Email: {email}, Password: {password}")
        checker  = PwnedChecker(callback)
        for email, password in credentials.items():
            checker.check_email(email)
            checker.check_password(password)

    def _run_DDOS(self, url: str, use_proxy: bool = False, callback: Callable = None):
        scanner = APIScrapper(callback)
        if use_proxy:
            scanner.set_proxy("http://127.0.0.1:8080")
        scanner.find_js_endpoints(url)
        api_endpoints = scanner.get_api_endpoints()
        threading.Thread(target=start_ddos, args=(url, api_endpoints, 100, 30, callback)).start() # Run attack in background

    def _run_unsigned_jwt(self, url: str, use_proxy: bool = True, callback: Callable = None):
        """
        Executes the Unsigned JWT attack.
        """
        if callback:
            callback("Running Unsigned JWT attack...")
        unsignedJWT()

    def _run_signed_jwt(self, url: str, use_proxy: bool = True, callback: Callable = None):
        """
        Executes the Signed JWT attack.
        """
        if callback:
            callback("Running Signed JWT attack...")
        signedJWT()

    def _run_request_intercept(self, url: str, use_proxy: bool = True, callback: Callable = None):
        """
        Starts request interception.
        """
        if callback:
            callback("Starting request interception...")
        requestIntercept()

    def _run_user_credentials(self, url: str, use_proxy: bool = True, callback: Callable = None):
        """
        Starts request interception.
        """
        if callback:
            callback("Starting User Credentials...")
        text = UserCredentials.db_drop(self=UserCredentials(url))
        callback(text.replace("},{","},\n{"))

    def _run_two_factor_authentificator(self, url: str, use_proxy: bool = True, callback: Callable = None):
        """
        Starts request interception.
        """
        if callback:
            callback("Starting Two Factor Authentificator...")
        output, text = TFA.login_as_wurstbrot(self=TFA(url))
        callback(text)

    def _run_sql_injection(self, url: str, use_proxy: bool = True, callback: Callable = None):
        """
        Starts sql injection.
        """
        if callback:
            callback("Starting sql injection...")
        username_input = "mc.safesearch@juice-sh.op"
        simulate_sql_injection(url, username_input, callback)

    def _run_xxe_data(self, url: str, use_proxy: bool = True, callback: Callable = None):
        """
        Starts XXE Data Access.
        """
        if callback:
            callback("Starting XXE Data Access...")
        payload_file = "Attacks/XXE_payload.xml"
        exploit_xxe(url, payload_file, callback)

    def _run_xss(self, url: str, use_proxy: bool = True, callback: Callable = None):
        """
        Starts Reflected XSS.
        """
        if callback:
            callback("Starting Reflected XSS...")
        malicious_script = "<iframe src='javascript:alert(`XSS6`)'></iframe>"
        simulate_reflected_xss(url, malicious_script, callback)
