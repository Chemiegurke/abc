import os
import sys
import logging

LOG_FILE = "logs/shadyshark_menu.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODULES = {
    "1": {"name": "Evil Twin WiFi", "script": "modules/evil_twin.py"},
    "2": {"name": "MITM-Detection & Autoban", "script": "modules/mitm_detection.py"},
    "3": {"name": "Zero-Day Exploit Auto-Loader", "script": "modules/exploit_loader.py"},
    "4": {"name": "Darknet & OSINT-Scanner", "script": "modules/osint_scanner.py"},
    "5": {"name": "Cloud Security Exploits", "script": "modules/cloud_security.py"},
    "6": {"name": "Active Directory Attacken", "script": "modules/ad_attack.py"},
    "7": {"name": "KI-gestützte Malware", "script": "modules/ai_malware.py"},
    "8": {"name": "SIEM Evasion & Anti-Detection", "script": "modules/siem_evasion.py"},
    "9": {"name": "Red Team Automation", "script": "modules/red_team_ai.py"},
    "10": {"name": "Web-GUI für Kontrolle & Live-Visualisierung", "script": "web_gui/dashboard.py"},
    "11": {"name": "Honeypot-Technologien", "script": "modules/honeypot.py"},
    "0": {"name": "Beenden", "script": None}
}

def display_menu():
    """
    Zeigt das Hauptmenü an.
    """
    print("\n🔥 ShadyShark Monster 5.2 – Hauptmenü 🔥")
    print("=====================================")
    for key, module in MODULES.items():
        print(f"[{key}] {module['name']}")
    print("=====================================")

def execute_module(choice):
    """
    Führt das gewählte Modul aus.
    """
    if choice in MODULES:
        module = MODULES[choice]
        if module["script"]:
            logging.info(f"🚀 Starte Modul: {module['name']}")
            os.system(f"python3 {module['script']}")
        else:
            logging.info("🛑 Beenden des Tools...")
            print("ShadyShark wird beendet...")
            sys.exit()
    else:
        print("❌ Ungültige Eingabe, bitte erneut versuchen.")

if __name__ == "__main__":
    while True:
        display_menu()
        user_choice = input("➡ Wähle eine Option: ")
        execute_module(user_choice)
