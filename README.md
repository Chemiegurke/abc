```markdown
# MEGA Client

Ein leistungsstarkes, benutzerfreundliches MEGA.nz-Client-Programm für
Windows mit **2FA-Login, Datei- & Ordnerverwaltung, Upload/Download mit Fortschrittsanzeige und Drag & Drop-Unterstützung**.

![MEGA Client Screenshot](https://via.placeholder.com/800x400.png?text=MEGA+Client+Preview)

## 🚀 Funktionen
✅ **Anmeldung mit 2FA-Unterstützung**  
✅ **Dateien & Ordner durchsuchen, anzeigen & verwalten**  
✅ **Uploads & Downloads mit Fortschrittsanzeige**  
✅ **Drag & Drop für einfache Dateiübertragung**  
✅ **Modernes UI mit Dark Mode**  
✅ **Einfache Installation & Nutzung**  

## 📥 Installation
### 1️⃣ Python & Abhängigkeiten installieren
Falls Python nicht installiert ist, lade es hier herunter: [Python Download](https://www.python.org/downloads/)

Dann installiere die benötigten Pakete:
```bash
pip install mega.py PyQt6
```

### 2️⃣ Das Programm starten
Speichere die Datei als `mega_client.py` und führe sie aus:
```bash
python mega_client.py
```

## 🔧 EXE-Datei erstellen (Windows)
Falls du eine eigenständige Windows-Anwendung ohne Python installieren willst, kannst du eine EXE-Datei erstellen:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed mega_client.py
```
Die fertige Datei liegt dann im `dist/` Ordner.

## 🖥️ Nutzung
1️⃣ **Anmelden** mit deinem MEGA.nz-Konto (inkl. 2FA, falls aktiviert).  
2️⃣ **Dateien durchsuchen, hochladen & herunterladen**.  
3️⃣ **Drag & Drop** zum einfachen Hochladen nutzen.  
4️⃣ **Dark Mode aktivieren** (automatisch integriert).  

## 🛠 Fehlerbehebung
Falls beim Erstellen der EXE ein `pathlib`-Fehler auftritt:
```bash
pip uninstall pathlib
```
Dann PyInstaller erneut ausführen.

## 📜 Lizenz
MIT License - Frei zur Nutzung und Modifikation.  

---
**Autor:** [Dein Name]  
**GitHub Repository:** [Hier Link einfügen]  

---
✨ Viel Spaß mit deinem MEGA-Client! 🚀
```

