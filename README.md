# 📚 Wortanalyse Web-App mit Streamlit

Diese Webanwendung erlaubt die umfassende Analyse von Textdokumenten (z. B. Episoden, Bücher oder Kapitel) in Bezug auf:

- Wortanzahl pro Datei
- Entwicklung neuer Wörter über Dateien hinweg
- Suche nach beliebigen Wörtern oder Wortgruppen
- Visualisierung der Häufigkeit als interaktive Diagramme
- Optional: Filterung von Stoppwörtern mittels externer Liste

---

## 🚀 Features

### 🔍 Interaktive Analyse

- **Häufigkeitsanalyse** von Begriffen über mehrere Episoden hinweg
- **Liniendiagramme** für Wortverläufe und Phrasen
- **Top-20-Wörter** als Balkendiagramm (optional ohne Stoppwörter)

### 📦 Eingabedaten

- Textdateien im Ordner `texte/`
- Jede Datei entspricht einer Episode (z. B. `001.txt`, `002.txt`, ...)
- Optional: eigene Stoppwortliste in `stoppworte/stopwords.txt`

### 📤 Ausgabe

- CSV-Download der Wortstatistiken pro Episode

---

## 🛠️ Lokale Installation

### Voraussetzungen

- Python 3.8+
- Empfohlenes virtuelles Environment

### Installation

```bash
# Repository klonen
git clone https://github.com/dasBeny/Wortanalyse-Web-App
cd wortanalyse-app

# Abhängigkeiten installieren
pip install -r requirements.txt
```



### App starten

```bash
streamlit run streamlit_app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

---

## 📁 Projektstruktur

```
wortanalyse-app/
├── streamlit_app.py               # Hauptanwendung
├── texte/                         # Eingabetexte (eine Datei pro Episode/Buch in .txt Format)
├── stoppworte/stopwords.txt      # Benutzerdefinierte Stoppwortliste
├── requirements.txt              # Python-Abhängigkeiten
└── README.md                     # Diese Datei
```

---

## ✅ To-Do / Erweiterungsideen

- Filterbare Visualisierungen (z. B. nach Worttyp)
- Wortstammerkennung / Lemmatisierung
- Sprachumschaltung (Deutsch ↔ Englisch)
- Option zur Auswahl einzelner Episoden

---

## 📄 Lizenz

MIT License – frei verwendbar mit Namensnennung.

---

## ✨ Demo Screenshot



---

Viel Spaß bei der Textanalyse! 📖
