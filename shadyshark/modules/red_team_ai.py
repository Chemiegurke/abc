import openai
import json
import logging

LOG_FILE = "logs/red_team_ai.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

OPENAI_API_KEY = "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"

if not OPENAI_API_KEY:
    logging.error("❌ Kein OpenAI API-Key gefunden!")
    raise ValueError("OpenAI API-Key fehlt!")

class RedTeamAutoGPT:
    """
    KI-gestütztes Penetration Testing mit automatischer Angriffspfad-Optimierung.
    """

    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def analyze_target(self, target_info):
        """
        Analysiert die Zielumgebung & generiert Angriffsszenarien.
        """
        logging.info("🔍 Analysiere Zielumgebung mit AutoGPT...")

        prompt = f"""
        Du bist ein fortschrittlicher Penetration-Testing-Assistent.
        Zielinformationen:
        {json.dumps(target_info, indent=4)}
        
        Erstelle einen Angriffspfad mit priorisierten Exploits & Angriffsmethoden.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": prompt}]
            )

            if "choices" in response and len(response["choices"]) > 0:
                attack_plan = response["choices"][0]["message"]["content"]
            else:
                logging.error("❌ OpenAI hat keine gültige Antwort zurückgegeben.")
                attack_plan = "Fehler: OpenAI konnte keine Antwort generieren."

        except Exception as e:
            logging.error(f"❌ Fehler bei der OpenAI-Anfrage: {e}")
            attack_plan = "Fehler: Keine Antwort von der KI."

        logging.info(f"🚀 Generierter Angriffspfad: {attack_plan}")
        return attack_plan

    def prioritize_exploits(self, vulnerabilities):
        """
        Nutzt KI zur Priorisierung der effektivsten Exploits.
        """
        logging.info("⚡ Priorisiere Exploits mit AutoGPT...")

        prompt = f"""
        Hier sind gefundene Sicherheitslücken:
        {json.dumps(vulnerabilities, indent=4)}

        Wähle die 3 effektivsten Exploits aus und begründe die Auswahl.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": prompt}]
            )

            if "choices" in response and len(response["choices"]) > 0:
                prioritized_exploits = response["choices"][0]["message"]["content"]
            else:
                logging.error("❌ OpenAI hat keine gültige Antwort zurückgegeben.")
                prioritized_exploits = "Fehler: OpenAI konnte keine Antwort generieren."

        except Exception as e:
            logging.error(f"❌ Fehler bei der OpenAI-Anfrage: {e}")
            prioritized_exploits = "Fehler: Keine Antwort von der KI."

        logging.info(f"🔥 Priorisierte Exploits: {prioritized_exploits}")
        return prioritized_exploits

if __name__ == "__main__":
    red_team_ai = RedTeamAutoGPT()

    test_target = {"OS": "Windows Server 2019", "Ports": [445, 3389], "Services": ["SMB", "RDP"]}
    test_vulnerabilities = [
        {"CVE": "CVE-2020-0796", "Service": "SMB"},
        {"CVE": "CVE-2021-34527", "Service": "Print Spooler"}
    ]

    attack_plan = red_team_ai.analyze_target(test_target)
    prioritized_exploits = red_team_ai.prioritize_exploits(test_vulnerabilities)

    print(f"\n🔹 Angriffspfad:\n{attack_plan}")
    print(f"\n🔥 Priorisierte Exploits:\n{prioritized_exploits}")
