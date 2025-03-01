# Flask Webserver für Kartenvisualisierung
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "ShadyShark Web GUI"

if __name__ == '__main__':
    app.run(debug=True)
