import os
import logging
import subprocess

LOG_FILE = "logs/honeypot.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class HoneypotManager:
    """
    Honeypot-Technologie zur Täuschung & Analyse von Angreifern.
    """

    def __init__(self):
        self.cowrie_path = "/opt/cowrie"
        self.dionaea_path = "/opt/dionaea"

        # Root-Check für iptables-Befehle
        if os.geteuid() != 0:
            logging.error("❌ Fehler: Skript muss als Root ausgeführt werden!")
            raise PermissionError("Dieses Skript muss mit Root-Rechten ausgeführt werden.")

    def start_cowrie(self):
        """
        Startet den Cowrie SSH- & Telnet-Honeypot.
        """
        if not os.path.exists(self.cowrie_path):
            logging.error("❌ Cowrie-Pfad nicht gefunden!")
            return

        logging.info("🚀 Starte Cowrie Honeypot...")
        try:
            subprocess.run(["./start.sh"], cwd=self.cowrie_path, check=True)
            logging.info("✅ Cowrie erfolgreich gestartet.")
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Fehler beim Starten von Cowrie: {e}")

    def start_dionaea(self):
        """
        Startet den Dionaea Exploit-Honeypot.
        """
        if not os.path.exists(self.dionaea_path):
            logging.error("❌ Dionaea-Pfad nicht gefunden!")
            return

        logging.info("🚀 Starte Dionaea Honeypot...")
        try:
            subprocess.Popen(["dionaea", "-D"], cwd=self.dionaea_path)
            logging.info("✅ Dionaea erfolgreich gestartet.")
        except Exception as e:
            logging.error(f"❌ Fehler beim Starten von Dionaea: {e}")

    def analyze_attacks(self):
        """
        Liest Logs und analysiert Angriffe.
        """
        logging.info("📊 Analysiere Honeypot-Logs...")
        cowrie_log = "/opt/cowrie/var/log/cowrie/cowrie.log"
        dionaea_log = "/opt/dionaea/var/log/dionaea.log"

        if os.path.exists(cowrie_log) and os.stat(cowrie_log).st_size > 0:
            with open(cowrie_log, "r", encoding="utf-8") as f:
                logs = f.readlines()[-10:]
                for log in logs:
                    if "login attempt" in log:
                        logging.warning(f"⚠️ Angriff erkannt in Cowrie: {log.strip()}")

        if os.path.exists(dionaea_log) and os.stat(dionaea_log).st_size > 0:
            with open(dionaea_log, "r", encoding="utf-8") as f:
                logs = f.readlines()[-10:]
                for log in logs:
                    if "exploit detected" in log:
                        logging.warning(f"⚠️ Angriff erkannt in Dionaea: {log.strip()}")

    def block_attacker(self, ip_address):
        """
        Sperrt Angreifer anhand der gesammelten Daten.
        """
        logging.info(f"🚫 Blockiere Angreifer mit IP: {ip_address}")

        try:
            subprocess.run(["iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"], check=True)
            logging.info(f"✅ IP {ip_address} erfolgreich blockiert.")
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Fehler beim Sperren der IP {ip_address}: {e}")

if __name__ == "__main__":
    honeypot = HoneypotManager()
    honeypot.start_cowrie()
    honeypot.start_dionaea()
    honeypot.analyze_attacks()
