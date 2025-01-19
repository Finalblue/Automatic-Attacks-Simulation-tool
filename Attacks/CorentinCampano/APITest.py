import requests
import re
from Attacks.CorentinCampano.APIScrapper import APIScrapper

class APITester:
    def __init__(self, callback = None):
        # emails and password found
        self.callback = callback or print
        self.credentials = {}  # Dictionnary {email: password}

    def extract_sensitive_info(self, response_text):
        """
        Extract emails and associated passwords from the response text.
        """
        # Regular expression to find emails
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = re.findall(email_pattern, response_text)

        # Regular expression to find password-like patterns
        password_pattern = r'(?i)(?:"password"|"passwd"|"pwd")\s*:\s*["\']([^"\']+)["\']'
        passwords = re.findall(password_pattern, response_text)

        # Associating emails and passwords if they appear in the same response
        if emails and passwords:
            for email, password in zip(emails, passwords):
                self.credentials[email] = password

    def test_endpoint(self, url):
        """
        Test a specific endpoint by sending requests and analyzing responses.
        """
        try:
            # Test GET method
            response = requests.get(url)
            self.callback(f"Testing GET {url} - Status Code: {response.status_code}")
            self.extract_sensitive_info(response.text)

            # Test other HTTP methods: PUT, DELETE
            methods = ['PUT', 'DELETE']
            for method in methods:
                response = requests.request(method, url)
                self.callback(f"Testing {method} {url} - Status Code: {response.status_code}")
                self.extract_sensitive_info(response.text)

            # Test POST method with XML payload
            xml_payload = """<?xml version='1.0' encoding='UTF-8'?>
            <note>
                <to>User</to>
                <from>Tester</from>
                <heading>API Test</heading>
                <body>This is a test payload</body>
            </note>"""
            headers = {'Content-Type': 'application/xml'}
            response = requests.post(url, data=xml_payload, headers=headers, timeout=10)
            self.callback(f"Testing POST {url} with XML payload - Status Code: {response.status_code}")
            self.extract_sensitive_info(response.text)

            # Check security headers
            headers = response.headers
            self.callback(f"Security headers for {url}:")
            security_headers = ["Strict-Transport-Security", "X-Content-Type-Options", "X-Frame-Options", "X-XSS-Protection"]
            for header in security_headers:
                if header in headers:
                     self.callback(f"  {header}: {headers[header]}")
                else:
                     self.callback(f"  {header}: Missing")

        except requests.exceptions.RequestException as e:
            self.callback(f"Error testing {url}: {e}")

    def get_credentials(self):
        """
        Return the dictionary of credentials found.
        """
        return self.credentials

# Example usage without GUI
# if __name__ == "__main__":
#     # Base URL of the site to test (e.g., OWASP Juice Shop)
#     target_url = "http://45.76.47.218:3000"  # Replace with your target URL

#     # Create an instance of the APIScrapper class to find API endpoints
#     scanner = APIScrapper()
#     scanner.find_js_endpoints(target_url)

#     # Get the API endpoints found
#     api_endpoints = scanner.get_api_endpoints()

#     tester = APITester()
#     # Test all found API endpoints
#     for endpoint in api_endpoints:
#         tester.test_endpoint(target_url + endpoint)

#     # Print credentials
#     credentials = tester.get_credentials()
#     print("Credentials found:")
#     for email, password in credentials.items():
#         print(f"  Email: {email}, Password: {password}")
