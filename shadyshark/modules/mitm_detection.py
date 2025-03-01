import scapy.all as scapy
import os
import subprocess
import logging
from collections import defaultdict

LOG_FILE = "logs/mitm_detection.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MITMDetector:
    """
    Überwacht das Netzwerk auf MITM-Angriffe und sperrt verdächtige Geräte.
    """

    def __init__(self, interface="wlan0"):
        self.interface = interface
        self.arp_cache = defaultdict(list)  # Historie statt Set für bessere Erkennung
        self.blocked_macs = set()

        # Root-Check
        if os.geteuid() != 0:
            print("❌ Dieses Skript muss als Root ausgeführt werden!")
            sys.exit(1)

        # Prüfen, ob die Netzwerkschnittstelle existiert
        if not self.check_interface():
            raise ValueError(f"❌ Fehler: Netzwerkschnittstelle {self.interface} existiert nicht.")

        # iptables-Regeln vorab bereinigen
        self.clear_firewall_rules()

    def check_interface(self):
        """ Überprüft, ob die angegebene Netzwerkschnittstelle existiert. """
        result = subprocess.run(["ip", "link", "show", self.interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0

    def detect_mitm(self, packet):
        """
        Analysiert ARP-Pakete und erkennt Spoofing-Versuche.
        """
        if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
            mac = packet[scapy.ARP].hwsrc
            ip = packet[scapy.ARP].psrc

            logging.info(f"🔍 ARP-Paket: {ip} → {mac}")

            if ip in self.arp_cache and mac not in self.arp_cache[ip]:
                logging.warning(f"⚠️ MITM-ANGRIFF ERKANNT: {ip} → {mac}")
                print(f"⚠️ MITM-ANGRIFF ERKANNT: {ip} → {mac}")

                if mac not in self.blocked_macs:
                    self.ban_attacker(mac, ip)

            self.arp_cache[ip].append(mac)  # Historie der MACs speichern

    def ban_attacker(self, mac_address, ip_address):
        """
        Sperrt den Angreifer mit iptables-Regeln.
        """
        logging.info(f"🚫 Sperre Angreifer mit MAC: {mac_address} & IP: {ip_address}")

        try:
            # Alte Sperrungen entfernen, um doppelte Regeln zu vermeiden
            subprocess.run(["iptables", "-D", "INPUT", "-m", "mac", "--mac-source", mac_address, "-j", "DROP"], stderr=subprocess.DEVNULL)
            subprocess.run(["iptables", "-D", "FORWARD", "-m", "mac", "--mac-source", mac_address, "-j", "DROP"], stderr=subprocess.DEVNULL)

            # Neue Sperren setzen
            subprocess.run(["iptables", "-A", "INPUT", "-m", "mac", "--mac-source", mac_address, "-j", "DROP"], check=True)
            subprocess.run(["iptables", "-A", "FORWARD", "-m", "mac", "--mac-source", mac_address, "-j", "DROP"], check=True)
            subprocess.run(["iptables", "-A", "FORWARD", "-s", ip_address, "-j", "DROP"], check=True)

            logging.info(f"✅ Angreifer {mac_address} (IP: {ip_address}) gesperrt.")
            self.blocked_macs.add(mac_address)
            print(f"🚫 Angreifer mit MAC {mac_address} & IP {ip_address} wurde gesperrt!")
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Fehler beim Sperren von {mac_address}: {e}")

    def clear_firewall_rules(self):
        """
        Bereinigt bestehende iptables-Regeln, um doppelte Sperrungen zu vermeiden.
        """
        subprocess.run(["iptables", "-F"], stderr=subprocess.DEVNULL)  # Alle Regeln leeren
        logging.info("✅ iptables-Regeln bereinigt.")

    def run(self):
        """
        Startet den Sniffer für ARP-Pakete.
        """
        print("🔍 Starte MITM-Detection...")
        logging.info("MITM-Detection gestartet...")
        scapy.sniff(iface=self.interface, store=False, prn=self.detect_mitm)

if __name__ == "__main__":
    try:
        detector = MITMDetector()
        detector.run()
    except Exception as e:
        logging.error(f"❌ Fehler: {e}")
        print(f"❌ Fehler: {e}")
