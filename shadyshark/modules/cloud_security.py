import requests
import subprocess
import json
import logging
import time

LOG_FILE = "logs/cloud_security.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

CLOUD_EXPLOIT_TOOLS = {
    "CloudSploit": "https://github.com/aquasecurity/cloudsploit",
    "Pacu": "https://github.com/RhinoSecurityLabs/pacu"
}

API_LEAK_CHECK_URL = "https://leakcheck.io/api/v1"
API_KEY = "DEIN_API_KEY"

class CloudSecurityScanner:
    """
    Automatische Schwachstellenanalyse für AWS, Azure & Google Cloud.
    """

    def __init__(self):
        self.api_keys = []

    def check_api_key_leaks(self, api_key):
        """
        Überprüft, ob ein API-Schlüssel öffentlich geleakt wurde.
        """
        logging.info(f"🔍 Überprüfe API-Key auf Leaks: {api_key}")

        params = {"key": API_KEY, "check": api_key}
        try:
            response = requests.get(API_LEAK_CHECK_URL, params=params, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Fehler bei API-Leak-Check: {e}")
            return False

        data = response.json()
        if data.get("leaked"):
            logging.warning(f"⚠️ GELEAKTER API-KEY GEFUNDEN: {api_key}")
            print(f"⚠️ GELEAKTER API-KEY GEFUNDEN: {api_key}")
            return True

        logging.info("✅ API-Key ist sicher.")
        return False

    def scan_cloud_misconfigurations(self):
        """
        Scan nach Fehlkonfigurationen in Cloud-Umgebungen mit CloudSploit.
        """
        logging.info("🚀 Starte Cloud-Sicherheitsprüfung mit CloudSploit...")

        try:
            result = subprocess.run(["cloudsploit", "scan", "--json"], capture_output=True, text=True, timeout=60)
            result.check_returncode()
            logging.info("✅ Scan erfolgreich abgeschlossen.")
            print("✅ Cloud-Sicherheitsprüfung abgeschlossen.")
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Fehler bei der Cloud-Sicherheitsprüfung: {e}")
            return None
        except subprocess.TimeoutExpired:
            logging.error("❌ CloudSploit-Scan hat das Zeitlimit überschritten.")
            return None

    def scan_aws_exploits(self):
        """
        Scannt AWS mit Pacu nach möglichen Exploits.
        """
        logging.info("🚀 Starte AWS Exploit-Scan mit Pacu...")

        try:
            result = subprocess.run(["pacu", "--run", "aws__enum_roles"], capture_output=True, text=True, timeout=60)
            result.check_returncode()
            logging.info("✅ AWS Exploit-Scan erfolgreich abgeschlossen.")
            print("✅ AWS Exploit-Scan erfolgreich abgeschlossen.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Fehler beim AWS Exploit-Scan: {e}")
            return None
        except subprocess.TimeoutExpired:
            logging.error("❌ Pacu-Scan hat das Zeitlimit überschritten.")
            return None

if __name__ == "__main__":
    scanner = CloudSecurityScanner()

    test_api_key = "12345-abcdef-67890"
    scanner.check_api_key_leaks(test_api_key)

    time.sleep(1)  # Schutz gegen API-Rate-Limits

    scanner.scan_cloud_misconfigurations()

    time.sleep(1)  # Schutz gegen Rate-Limits

    scanner.scan_aws_exploits()
