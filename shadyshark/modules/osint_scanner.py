import requests
import logging
import json
import time

# Logging konfigurieren
LOG_FILE = "logs/osint_scanner.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# API-URLs & Schlüssel
HIBP_API = "https://haveibeenpwned.com/api/v3/breachedaccount/"
ABUSEIPDB_API = "https://api.abuseipdb.com/api/v2/check"
GEOIP_API = "http://ip-api.com/json/"

HIBP_API_KEY = "DEIN_API_KEY"
ABUSEIPDB_KEY = "DEIN_API_KEY"

class OSINTScanner:
    """
    Darknet & OSINT-Scanner für gestohlene Passwörter, kompromittierte IPs & GeoIP-Tracking.
    """

    def __init__(self):
        self.session = requests.Session()

    def check_leaked_passwords(self, email):
        """
        Überprüft, ob eine E-Mail in Darknet-Datenbanken geleakt wurde.
        """
        headers = {
            "User-Agent": "ShadyShark",
            "hibp-api-key": HIBP_API_KEY
        }

        try:
            response = self.session.get(f"{HIBP_API}{email}", headers=headers, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Fehler bei HIBP-Check: {e}")
            return None

        if response.status_code == 200:
            logging.warning(f"⚠️ GELEAKTE DATEN GEFUNDEN für {email}")
            print(f"⚠️ GELEAKTE DATEN GEFUNDEN für {email}")
            return response.json()

        logging.info(f"✅ Keine Leaks für {email}")
        return None

    def check_threat_intelligence(self, ip):
        """
        Überprüft, ob eine IP in Threat Intelligence-Datenbanken gelistet ist.
        """
        headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
        params = {"ipAddress": ip, "maxAgeInDays": "90"}

        try:
            response = self.session.get(ABUSEIPDB_API, headers=headers, params=params, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Fehler beim Threat Intelligence-Check: {e}")
            return None

        data = response.json()
        if data.get("data", {}).get("abuseConfidenceScore", 0) > 50:
            logging.warning(f"⚠️ VERDÄCHTIGE IP GEFUNDEN: {ip}")
            print(f"⚠️ VERDÄCHTIGE IP GEFUNDEN: {ip}")
            return data

        logging.info(f"✅ Keine Bedrohung für IP {ip}")
        return None

    def geoip_lookup(self, ip):
        """
        GeoIP-Tracking zur Standortanalyse von Angreifern.
        """
        try:
            response = self.session.get(f"{GEOIP_API}{ip}", timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Fehler beim GeoIP-Tracking: {e}")
            return None

        geo_data = response.json()
        location = f"{geo_data.get('city', 'Unbekannt')}, {geo_data.get('country', 'Unbekannt')}"
        logging.info(f"🌍 Standort von {ip}: {location}")
        print(f"🌍 Standort von {ip}: {location}")

        return geo_data

if __name__ == "__main__":
    scanner = OSINTScanner()

    test_email = "example@example.com"
    test_ip = "192.168.1.100"

    # Wartezeit zwischen API-Anfragen (Schutz vor Rate-Limits)
    scanner.check_leaked_passwords(test_email)
    time.sleep(1)

    scanner.check_threat_intelligence(test_ip)
    time.sleep(1)

    scanner.geoip_lookup(test_ip)
