import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ASR Benchmark Dashboard", page_icon="🎙️", layout="wide")

# --- Project USP ---
with st.sidebar:
    st.header("Project USP 🚀")
    st.markdown("""
    **What makes this ASR Benchmark unique:**
    
    1. **Context-Aware Evaluation**: We don't just measure Word Error Rate (WER); we specifically evaluate performance on local Indian contexts and regional entities (like Bangalore neighborhoods).
    2. **Holistic Trade-offs**: Analyzes the delicate balance between high transcription accuracy and low-latency real-time performance.
    3. **Multi-Architecture Support**: Seamlessly evaluates cloud-based APIs (Deepgram, Groq), specialized regional models (Sarvam AI), and local offline models (Whisper).
    4. **Actionable Analytics**: Transforms raw transcriptions into structured intelligence with fuzzy matching for domain-specific entity extraction.
    """)
    st.info("Run this app using:\n`streamlit run dashboard.py`")

st.title("🎙️ ASR Benchmark Interactive Dashboard")
st.markdown("A comprehensive evaluation of Speech Recognition models focusing on accuracy (WER), speed (Latency), and domain-specific extraction (Locality).")

DATA_PATH = "reports/asr_benchmark_results.xlsx"

@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        return None
    return pd.read_excel(DATA_PATH)

df = load_data()

if df is None:
    st.warning(f"No benchmark data found at `{DATA_PATH}`. Please run `python app.py` first to generate the report.")
    st.stop()

# Clean up model names for display
if "model" in df.columns:
    df["model_display"] = df["model"].astype(str).str.replace("_", " ")

# --- Overview Section ---
st.header("1. 📊 Executive Summary")

summary_df = df.groupby("model_display").agg(
    Avg_WER=("wer", "mean"),
    Avg_Fuzzy_Score=("fuzzy_score", "mean"),
    Locality_Accuracy=("locality_correct", "mean"),
    Avg_Latency_sec=("latency_seconds", "mean")
).reset_index()

# Format summary
summary_df["Avg_WER"] = summary_df["Avg_WER"].round(4)
summary_df["Avg_Fuzzy_Score"] = summary_df["Avg_Fuzzy_Score"].round(2)
summary_df["Locality_Accuracy"] = (summary_df["Locality_Accuracy"] * 100).round(1).astype(str) + "%"
summary_df["Avg_Latency_sec"] = summary_df["Avg_Latency_sec"].round(2)

st.dataframe(summary_df, width="stretch", hide_index=True)

st.divider()

# --- Visualizations ---
col1, col2 = st.columns(2)

with col1:
    st.header("2. 📉 Word Error Rate (WER)")
    st.markdown("Lower is better. Measures transcription accuracy.")
    fig_wer = px.bar(
        summary_df, 
        x="model_display", 
        y="Avg_WER", 
        color="model_display",
        text_auto=True,
        labels={"Avg_WER": "Average WER", "model_display": "Model"}
    )
    fig_wer.update_layout(showlegend=False)
    st.plotly_chart(fig_wer, width="stretch")

with col2:
    st.header("3. ⚡ Latency Comparison")
    st.markdown("Lower is better. Measures transcription speed in seconds.")
    fig_lat = px.bar(
        summary_df, 
        x="model_display", 
        y="Avg_Latency_sec", 
        color="model_display",
        text_auto=True,
        labels={"Avg_Latency_sec": "Avg Latency (s)", "model_display": "Model"}
    )
    fig_lat.update_layout(showlegend=False)
    st.plotly_chart(fig_lat, width="stretch")

st.divider()

# --- Locality Accuracy ---
st.header("4. 📍 Locality Recognition Accuracy")
st.markdown("Higher is better. Percentage of times the model correctly transcribed the target neighborhood.")

# Calculate percentages for pie/donut charts
loc_data = df.groupby(["model_display", "locality_correct"]).size().reset_index(name="count")
models = df["model_display"].unique()

# Create columns for donut charts
cols = st.columns(len(models))
for i, model in enumerate(models):
    with cols[i]:
        m_data = loc_data[loc_data["model_display"] == model]
        fig_donut = px.pie(
            m_data, 
            values="count", 
            names="locality_correct", 
            hole=0.6,
            color="locality_correct",
            color_discrete_map={True: "#22c55e", False: "#ef4444"},
            title=model
        )
        fig_donut.update_layout(showlegend=False, margin=dict(t=30, b=0, l=0, r=0))
        # Add annotation in center
        correct_count = m_data[m_data["locality_correct"] == True]["count"].sum() if True in m_data["locality_correct"].values else 0
        total_count = m_data["count"].sum()
        pct = (correct_count / total_count * 100) if total_count > 0 else 0
        
        fig_donut.add_annotation(text=f"{pct:.0f}%", x=0.5, y=0.5, font_size=20, showarrow=False)
        st.plotly_chart(fig_donut, width="stretch")

st.divider()

# --- Failure Analysis Section ---
st.header("5. 🔍 Failure Analysis")
st.markdown("Investigate specific audio files where models struggled with High WER (> 0.5).")

failures = df[df["wer"] > 0.5]

if failures.empty:
    st.success("No failures found for this criteria! 🎉")
else:
    # Select columns to show
    cols_to_show = ["audio_file", "model_display", "transcription", "reference_text", "expected_locality", "wer", "fuzzy_score"]
    available_cols = [c for c in cols_to_show if c in failures.columns]
    
    st.dataframe(
        failures[available_cols].style.map(
            lambda x: "background-color: #4a0404; color: #ffcccc;" if pd.isna(x) or x == '' or x is None else ""
        ),
        width="stretch",
        hide_index=True
    )
