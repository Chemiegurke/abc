import subprocess
import json
import logging
import time

LOG_FILE = "logs/ad_attack.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

BLOODHOUND_COLLECTOR = "/usr/bin/sharpHound.exe"  # Pfad zur BloodHound Collection Binary

class ActiveDirectoryAttack:
    """
    Automatische Abfrage von AD-Strukturen, Berechtigungen und Privilege Escalation.
    """

    def __init__(self, domain_controller, username, password):
        self.domain_controller = domain_controller
        self.username = username
        self.password = password

    def collect_ad_data(self):
        """
        Führt BloodHound-Datensammlung aus und speichert JSON-Daten für die Analyse.
        """
        logging.info("🚀 Starte BloodHound-Datensammlung für AD...")

        command = [
            BLOODHOUND_COLLECTOR, "-c", "All", "-d", self.domain_controller, "-u", self.username, "-p", self.password
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            result.check_returncode()
            logging.info("✅ AD-Daten erfolgreich extrahiert.")
            print("✅ AD-Daten erfolgreich extrahiert.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Fehler bei der AD-Datensammlung: {e}")
            return None
        except subprocess.TimeoutExpired:
            logging.error("❌ BloodHound-Scan hat das Zeitlimit überschritten.")
            return None

    def analyze_privilege_escalation(self, bloodhound_json):
        """
        Analysiert Privilege Escalation-Pfade innerhalb von AD.
        """
        logging.info("🔍 Analysiere AD-Berechtigungen auf Schwachstellen...")

        try:
            data = json.loads(bloodhound_json)
        except json.JSONDecodeError as e:
            logging.error(f"❌ Fehler beim Parsen der BloodHound-Daten: {e}")
            return

        escalation_paths = [
            obj["AdminTo"] for obj in data.get("data", []) if "AdminTo" in obj
        ]

        if escalation_paths:
            logging.warning(f"⚠️ Privilege Escalation-Pfade gefunden: {escalation_paths}")
            print(f"⚠️ Privilege Escalation-Pfade gefunden: {escalation_paths}")
        else:
            logging.info("✅ Keine kritischen Privilege Escalation-Pfade erkannt.")

if __name__ == "__main__":
    ad_attacker = ActiveDirectoryAttack("ad.example.com", "admin", "passwort123")

    ad_data = ad_attacker.collect_ad_data()

    time.sleep(1)  # Schutz gegen mögliche Rate-Limits

    if ad_data:
        ad_attacker.analyze_privilege_escalation(ad_data)
