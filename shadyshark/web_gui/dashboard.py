from flask import Flask, render_template, jsonify
import os
import json
import logging

LOG_FILE = "logs/web_gui.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

# Beispielhafte Angreifer-Daten für die Kartenvisualisierung
attack_data = [
    {"ip": "192.168.1.10", "location": "Berlin, Deutschland", "status": "Active"},
    {"ip": "203.0.113.50", "location": "New York, USA", "status": "Under Analysis"},
    {"ip": "8.8.8.8", "location": "Google HQ, USA", "status": "Blocked"},
]

@app.route("/")
def dashboard():
    if not os.path.exists("templates/dashboard.html"):
        logging.error("❌ Template 'dashboard.html' fehlt!")
        return "<h1>Fehler: Dashboard nicht gefunden!</h1>", 404
    return render_template("dashboard.html")

@app.route("/logs")
def get_logs():
    logs = []
    log_files = ["logs/evil_twin.log", "logs/mitm_detection.log", "logs/exploit_loader.log"]

    for log_file in log_files:
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                logs.extend(f.readlines()[-10:])  # Zeigt die letzten 10 Log-Einträge
        else:
            logs.append(f"⚠️ Log-Datei nicht gefunden: {log_file}")

    return jsonify({"logs": logs})

@app.route("/attack_data")
def get_attack_data():
    try:
        return jsonify({"attacks": attack_data})
    except Exception as e:
        logging.error(f"❌ Fehler bei der JSON-Antwort: {e}")
        return jsonify({"error": "Fehler bei der Datenverarbeitung"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
