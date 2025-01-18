import requests
from APIScrapper import APIScanner

# Function to test a specific endpoint
def test_endpoint(url):
    try:
        # Test GET method
        response = requests.get(url)
        print(f"Testing GET {url} - Status Code: {response.status_code}")

        # Test other HTTP methods: POST, PUT, DELETE
        methods = ['PUT', 'DELETE']
        for method in methods:
            response = requests.request(method, url)
            print(f"Testing {method} {url} - Status Code: {response.status_code}")

        # Test POST method with XML file
        xml_payload = """<?xml version='1.0' encoding='UTF-8'?>
        <note>
            <to>User</to>
            <from>Tester</from>
            <heading>API Test</heading>
            <body>This is a test payload</body>
        </note>"""
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(url, data=xml_payload, headers=headers)
        print(f"Testing POST {url} with XML payload - Status Code: {response.status_code}")

        # Check security headers
        headers = response.headers
        print(f"Security headers for {url}:")
        security_headers = ["Strict-Transport-Security", "X-Content-Type-Options", "X-Frame-Options", "X-XSS-Protection"]
        for header in security_headers:
            if header in headers:
                print(f"  {header}: {headers[header]}")
            else:
                print(f"  {header}: Missing")

    except requests.exceptions.RequestException as e:
        print(f"Error testing {url}: {e}")

# Example usage without GUI
if __name__ == "__main__":
    # Base URL of the site to test (e.g., OWASP Juice Shop)
    target_url = "http://45.76.47.218:3000"  # Replace with your target URL

    # Create an instance of the APIScanner class to find API endpoints
    scanner = APIScanner()
    scanner.find_js_endpoints(target_url)

    # Get the API endpoints found
    api_endpoints = scanner.get_api_endpoints()

    # Test all found API endpoints
    for endpoint in api_endpoints:
        test_endpoint(target_url + endpoint)