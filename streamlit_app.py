import streamlit as st
import pandas as pd
import re
from collections import Counter
from pathlib import Path
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📚 Wortanalyse in Textdateien")

# Pfade zu Text- und Stoppwortverzeichnis
TEXT_DIR = Path("texte")  # Stelle sicher, dass ein Ordner namens 'texte' mit .txt-Dateien existiert
STOPWORD_FILE = Path("stopwords.txt")
text_files = list(TEXT_DIR.glob("*.txt"))

# Stoppwörter aus Datei laden
if STOPWORD_FILE.exists():
    stopwords = set(word.strip().lower() for word in STOPWORD_FILE.read_text(encoding="utf-8").splitlines() if word.strip())
else:
    stopwords = set()
    st.warning("⚠️ Keine gültige Stoppwortdatei unter 'stoppworte/stopwords.txt' gefunden. Es werden keine Stoppwörter gefiltert.")

# Funktion zur Textbereinigung
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[\W_]+", " ", text)  # ersetzt Nicht-Wortzeichen durch Leerzeichen
    return text

if text_files:
    book_stats = []
    global_word_counter = Counter()
    new_words_set = set()

    cleaned_texts = {}

    for file in text_files:
        text = file.read_text(encoding="utf-8")
        cleaned = clean_text(text)
        cleaned_texts[file.name] = cleaned

        words = cleaned.split()
        filtered_words = [w for w in words if w not in stopwords]
        word_count = len(words)
        unique_words = set(filtered_words)
        new_words = unique_words - new_words_set
        new_words_set.update(unique_words)

        book_stats.append({
            "Dateiname": file.name,
            "Wörter gesamt": word_count,
            "Einzigartige Wörter": len(unique_words),
            "Neue Wörter (kumulativ)": len(new_words)
        })

        global_word_counter.update(filtered_words)

    # Zeige Statistik je Buch
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

    # Mehrwortsuche (kombinierte Phrasen)
    st.subheader("🔍 Phrasensuche")
    phrase_input = st.text_area("Gib eine oder mehrere Wortgruppen (durch Kommas getrennt) ein, z. B.: feuer, schwarzer rauch")

    if phrase_input:
        phrases = [p.strip().lower() for p in phrase_input.split(",") if p.strip()]
        data = []

        for i, (file_name, cleaned) in enumerate(cleaned_texts.items(), start=1):
            for phrase in phrases:
                count = cleaned.count(" "+phrase+" ")
                data.append({"Episode": i, "Dateiname": file_name, "Phrase": phrase, "Anzahl": count})

        df_phrases = pd.DataFrame(data)
        fig_phrases = px.line(df_phrases, x="Episode", y="Anzahl", color="Phrase", markers=True,
                              title="📈 Häufigkeit der gewählten Phrasen über alle Episoden",
                              labels={"Anzahl": "Anzahl", "Episode": "Episode"})
        st.plotly_chart(fig_phrases, use_container_width=True)

    # Top 20 Wörter insgesamt
    st.subheader("🏆 Top 20 häufigste Wörter insgesamt (ohne Stoppwörter)")
    most_common_df = pd.DataFrame(global_word_counter.most_common(20), columns=["Wort", "Anzahl"])
    fig_common = px.bar(most_common_df, x="Wort", y="Anzahl", title="🏅 Häufigste Wörter", text="Anzahl")
    st.plotly_chart(fig_common, use_container_width=True)

    # Optional: Download als CSV
    csv = df_stats.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Lade Statistiken als CSV herunter", csv, "buchstatistiken.csv", "text/csv")
else:
    st.warning("❗ Keine Textdateien im Ordner 'texte' gefunden.")
