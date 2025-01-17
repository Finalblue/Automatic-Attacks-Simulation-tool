import subprocess
import logging


class NmapScanner:
    def __init__(self, target_url):
        self.target_url = target_url

    def scan(self):
        """Perform an Nmap scan."""
        try:
            result = subprocess.run(
                ["nmap", "-sV", self.target_url],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                logging.info("[+] Nmap scan succeeded.")
                return {"status": "success", "details": result.stdout}
            else:
                logging.warning("[-] Nmap scan completed with warnings/errors.")
                return {"status": "failed", "details": result.stderr}
        except subprocess.TimeoutExpired:
            logging.error("[-] Nmap scan timed out.")
            return {"status": "failed", "details": "Scan timed out."}
        except Exception as e:
            logging.error(f"[-] Nmap scan failed: {e}")
            return {"status": "failed", "details": str(e)}
