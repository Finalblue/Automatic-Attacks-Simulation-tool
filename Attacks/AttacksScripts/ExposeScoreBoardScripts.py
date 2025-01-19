import asyncio
from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster
import json

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 8080
JUICE_URL_SNIPPET = "45.76.47.218:3000"

class ExposeScoreBoard:
    def response(self, flow: http.HTTPFlow):
        try:
            # Check if the response is for the Score Board API
            if "/rest/score-board" in flow.request.pretty_url:
                # Parse and print the JSON response
                response_content = json.loads(flow.response.text)
                print("[*] Extracted Score Board Data:")
                print(json.dumps(response_content, indent=4))
        except Exception as e:
            print(f"[!] Error processing score board response: {e}")

async def run_proxy():
    opts = options.Options(listen_host=LISTEN_HOST, listen_port=LISTEN_PORT)
    m = DumpMaster(opts)
    m.addons.add(ExposeScoreBoard())
    try:
        await m.run()
    except KeyboardInterrupt:
        print("[!] Proxy interrupted.")
    finally:
        m.shutdown()

def expose_score_board():
    asyncio.run(run_proxy())