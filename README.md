# 📚 Wortanalyse Web App

Diese Anwendung analysiert den Wortschatz einer umfangreichen Textsammlung (z. B. Romanreihen, Episodenliteratur, Fachtexte etc.) und visualisiert statistische Daten zu Wortverteilungen, Phrasenhäufigkeit und individuellen Entwicklungen über die Zeit.

Die Anwendung nutzt **Google Drive** zur sicheren Einbindung urheberrechtlich geschützter Texte, ohne sie öffentlich zugänglich zu machen.

---

## 🚀 Funktionen

- 📈 Visualisierung der Wortanzahl pro Episode
- 🧠 Zählung einzigartiger und neuer Wörter über Zeit
- 🔍 Phrasensuche (mehrere Begriffe gleichzeitig analysierbar)
- 🏆 Anzeige der 20 häufigsten Wörter (ohne Stoppwörter)
- 📥 Download der Statistik als CSV

---

## 🔧 Installation

### 1. Repository klonen

```bash
git clone https://github.com/dein-user/Wortanalyse-Web-App.git
cd Wortanalyse-Web-App
```

### 2. Abhängigkeiten installieren

Erstelle am besten ein virtuelles Environment und installiere dann:

```bash
pip install -r requirements.txt
```

### 3. `.streamlit/secrets.toml` einrichten

Diese App verwendet einen **Google Service Account**, um auf deine privaten `.txt`-Dateien in einem bestimmten Google-Drive-Ordner zuzugreifen.

Füge unter `.streamlit/secrets.toml` folgende Struktur ein:

```toml
[google]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = """-----BEGIN PRIVATE KEY-----
DEIN
GEHEIMER
KEY
HIER
-----END PRIVATE KEY-----"""
client_email = "xyz@dein-projekt.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
```

> 🎯 Den JSON-Service-Account-Schlüssel erhältst du über die [Google Cloud Console](https://console.cloud.google.com/). Vergiss nicht, den Ordner mit deinen `.txt`-Dateien für den Service-Account freizugeben!

---

## 📁 Ordnerstruktur

- `streamlit_app.py` – Hauptlogik der App
- `requirements.txt` – Python-Abhängigkeiten
- `.streamlit/secrets.toml` – **nicht committen!** (geheim)
- `stopwords.txt` – optionale Stoppwortliste

---

## ☁️ Deployment auf Streamlit Cloud

Diese App funktioniert out-of-the-box auf [Streamlit Cloud](https://streamlit.io/cloud):

1. Repository mit GitHub verknüpfen
2. In Streamlit Cloud auf „Add App“ klicken
3. Bei „Secrets“ den Inhalt aus deiner `secrets.toml` einfügen
4. Fertig ✅

---

## ⚠️ Hinweis zu Urheberrechten

Diese App verarbeitet Texte, die urheberrechtlich geschützt sein können. Die Textdateien selbst werden **nicht veröffentlicht** oder zugänglich gemacht.  
Der Zugriff erfolgt nur über **privaten Google Drive**, kontrolliert durch den App-Betreiber.

---

## 🧪 Beispielhafte Einsatzszenarien

- Analyse von Romanserien, z. B. Fantasy- oder Sci-Fi-Reihen
- Sprachentwicklungen in Tagebüchern oder Briefsammlungen
- Fachtextanalysen für Wissenschaft, Unterricht, Forschung

---

## 📜 Lizenz

MIT License – siehe [LICENSE](LICENSE)

---

## ✨ Autor

**Ben (a.k.a. dasBeny)**  
[github.com/dasBeny](https://github.com/dasBeny)
