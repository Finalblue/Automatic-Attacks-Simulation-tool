import asyncio
from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster
import json

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 8080
JUICE_URL_SNIPPET = "45.76.47.218:3000"

class RetrieveOrders:
    def request(self, flow: http.HTTPFlow):
        try:
            # Check if the request targets the Orders API
            if "/api/Orders" in flow.request.pretty_url and flow.request.method == "GET":
                # Optionally modify the request to bypass restrictions (e.g., user ID or token)
                print("[*] Intercepted Orders API request:")
                print(flow.request.pretty_url)

        except Exception as e:
            print(f"[!] Error processing orders request: {e}")

    def response(self, flow: http.HTTPFlow):
        try:
            # Check if the response is for the Orders API
            if "/api/Orders" in flow.request.pretty_url:
                # Parse and print the JSON response
                response_content = json.loads(flow.response.text)
                print("[*] Extracted Orders Data:")
                print(json.dumps(response_content, indent=4))
        except Exception as e:
            print(f"[!] Error processing orders response: {e}")

async def run_proxy():
    opts = options.Options(listen_host=LISTEN_HOST, listen_port=LISTEN_PORT)
    m = DumpMaster(opts)
    m.addons.add(RetrieveOrders())
    try:
        await m.run()
    except KeyboardInterrupt:
        print("[!] Proxy interrupted.")
    finally:
        m.shutdown()

def retrieve_orders():
    asyncio.run(run_proxy())
