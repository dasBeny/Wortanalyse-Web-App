import streamlit as st
import pandas as pd
import re
from collections import Counter
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import tempfile
import json
import os
import plotly.express as px

# ----- Konfiguration -----
st.set_page_config(layout="wide")
st.title("📚 Wortanalyse in Textdateien")
FOLDER_ID = "1-r8Qj_E_SoJEpLzpQTkIho2-GudLlIN7"

# ----- Stoppliste laden -----
STOPWORD_FILE = "stopwords.txt"
try:
    with open(STOPWORD_FILE, encoding="utf-8") as f:
        stopwords = set(line.strip().lower() for line in f if line.strip())
except FileNotFoundError:
    stopwords = set()
    st.warning("⚠️ Keine gültige Stoppliste gefunden. Es werden keine Stoppwörter gefiltert.")

# ----- Google Drive Zugriff -----

@st.cache_resource
def load_files_from_drive():
    try:
        credentials = service_account.Credentials.from_service_account_info(
            dict(st.secrets["google"]),
            scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )
        service = build("drive", "v3", credentials=credentials)

        # Suche nach .txt-Dateien im Ordner
        query = f"'{FOLDER_ID}' in parents and mimeType='text/plain' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])

        texts = {}
        for file in files:
            file_id = file["id"]
            file_name = file["name"]
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            texts[file_name] = fh.read().decode("utf-8")

        return texts

    except Exception as e:
        st.error(f"❌ Fehler beim Laden von Dateien: {e}")
        return {}


# ----- Text-Bereinigung -----
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[\W_]+", " ", text)
    return text

# ----- Hauptverarbeitung -----
texts = load_files_from_drive()

if texts:
    book_stats = []
    global_word_counter = Counter()
    new_words_set = set()
    cleaned_texts = {}

    for idx, (file_name, raw_text) in enumerate(texts.items(), start=1):
        cleaned = clean_text(raw_text)
        cleaned_texts[file_name] = cleaned

        words = cleaned.split()
        filtered_words = [w for w in words if w not in stopwords]
        word_count = len(words)
        unique_words = set(filtered_words)
        new_words = unique_words - new_words_set
        new_words_set.update(unique_words)

        book_stats.append({
            "Dateiname": file_name,
            "Wörter gesamt": word_count,
            "Einzigartige Wörter": len(unique_words),
            "Neue Wörter (kumulativ)": len(new_words)
        })

        global_word_counter.update(filtered_words)

    # ---- Statistiken anzeigen ----
    df_stats = pd.DataFrame(book_stats)
    st.subheader("📈 Buchstatistiken")

    fig_words = px.line(df_stats.reset_index(), x=df_stats.index + 1, y="Wörter gesamt", markers=True,
                        labels={"index": "Episode", "Wörter gesamt": "Wörter"},
                        title="📊 Wörter pro Episode")
    st.plotly_chart(fig_words, use_container_width=True)

    fig_unique = px.line(df_stats.reset_index(), x=df_stats.index + 1, y="Einzigartige Wörter", markers=True,
                         labels={"index": "Episode", "Einzigartige Wörter": "Einzigartige Wörter"},
                         title="🧠 Einzigartige Wörter pro Episode")
    st.plotly_chart(fig_unique, use_container_width=True)

    # ---- Phrasensuche ----
    st.subheader("🔍 Phrasensuche")
    phrase_input = st.text_area("Gib eine oder mehrere Wortgruppen (durch Kommas getrennt) ein, z. B.: feuer, schwarzer rauch")

    if phrase_input:
        phrases = [p.strip().lower() for p in phrase_input.split(",") if p.strip()]
        data = []

        for i, (file_name, cleaned) in enumerate(cleaned_texts.items(), start=1):
            for phrase in phrases:
                count = cleaned.count(" " + phrase + " ")
                data.append({"Episode": i, "Dateiname": file_name, "Phrase": phrase, "Anzahl": count})

        df_phrases = pd.DataFrame(data)
        fig_phrases = px.line(df_phrases, x="Episode", y="Anzahl", color="Phrase", markers=True,
                              title="📈 Häufigkeit der gewählten Phrasen über alle Episoden",
                              labels={"Anzahl": "Anzahl", "Episode": "Episode"})
        st.plotly_chart(fig_phrases, use_container_width=True)

    # ---- Top-Wörter anzeigen ----
    st.subheader("🏆 Top 20 häufigste Wörter insgesamt (ohne Stoppwörter)")
    most_common_df = pd.DataFrame(global_word_counter.most_common(20), columns=["Wort", "Anzahl"])
    fig_common = px.bar(most_common_df, x="Wort", y="Anzahl", title="🏅 Häufigste Wörter", text="Anzahl")
    st.plotly_chart(fig_common, use_container_width=True)

    # ---- Download ----
    csv = df_stats.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Lade Statistiken als CSV herunter", csv, "buchstatistiken.csv", "text/csv")
else:
    st.warning("❗ Keine Textdateien gefunden oder Ordner-ID ist ungültig.")
