import streamlit as st
import os
import json
import base64
import requests
from dotenv import load_dotenv

# ── Load environment ──────────────────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("SARVAM_API_KEY", "")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sarvam AI Tester",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

/* Base Styles & Font override */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Full Screen Layout */
[data-testid="stMainBlockContainer"], .block-container {
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* Background mesh gradient */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(20, 184, 166, 0.12) 0%, transparent 45%),
                linear-gradient(135deg, #09090e 0%, #11101e 100%) !important;
    background-attachment: fixed !important;
}

/* Glassmorphism Sidebar */
[data-testid="stSidebar"] {
    background-color: rgba(9, 9, 14, 0.75) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.08) !important;
}

/* Custom CSS Card class for raw HTML cards */
.card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.card:hover {
    border-color: rgba(124, 58, 237, 0.35);
    box-shadow: 0 8px 32px 0 rgba(124, 58, 237, 0.12);
    transform: translateY(-2px);
}

/* Streamlit Container border targeting */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    backdrop-filter: blur(16px) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25) !important;
    transition: all 0.3s ease !important;
    margin-bottom: 20px !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(124, 58, 237, 0.25) !important;
}

/* Badges */
.badge-ok {
    background: rgba(16, 185, 129, 0.15) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 12px;
}
.badge-err {
    background: rgba(239, 68, 68, 0.15) !important;
    color: #f87171 !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 12px;
}

.key-ok {
    color: #34d399;
    font-weight: 600;
    font-size: 14px;
    margin-top: 8px;
}
.key-err {
    color: #f87171;
    font-weight: 600;
    font-size: 14px;
    margin-top: 8px;
}

/* Response Box */
.response-box {
    background: rgba(7, 6, 15, 0.85) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px;
    padding: 18px;
    font-family: 'Fira Code', 'Courier New', monospace !important;
    font-size: 13px;
    color: #a5f3fc;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 320px;
    overflow-y: auto;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5);
    margin-top: 8px;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

/* Subheadings & Labels */
p, label, span, div, li {
    color: #cbd5e1 !important;
}

/* Buttons styling */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.3) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    width: 100% !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5) !important;
    background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}
.stButton > button:active, .stDownloadButton > button:active {
    transform: translateY(1px) !important;
}

/* Input Fields overrides */
div[data-baseweb="input"],
div[data-baseweb="base-input"],
div[data-baseweb="textarea"],
div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="input"]:hover,
div[data-baseweb="base-input"]:hover,
div[data-baseweb="textarea"]:hover,
div[data-baseweb="select"] > div:hover {
    border-color: rgba(255, 255, 255, 0.2) !important;
    background-color: rgba(255, 255, 255, 0.06) !important;
}
div[data-baseweb="input"]:focus-within,
div[data-baseweb="base-input"]:focus-within,
div[data-baseweb="textarea"]:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.25) !important;
    background-color: rgba(255, 255, 255, 0.08) !important;
}

/* Style the actual inputs/textareas nested inside */
input,
textarea {
    color: #f8fafc !important;
    background-color: transparent !important;
}

/* Also style select text and select icon color to look clean */
div[data-baseweb="select"] span,
div[data-baseweb="select"] svg {
    color: #cbd5e1 !important;
}

/* Dropdown list items styling */
div[role="listbox"] {
    background-color: #0f0f1b !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
}
div[role="option"] {
    color: #cbd5e1 !important;
    transition: all 0.2s ease !important;
}
div[role="option"]:hover, div[role="option"][aria-selected="true"] {
    background-color: rgba(124, 58, 237, 0.15) !important;
    color: #c084fc !important;
}

/* File Uploader override */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 2px dashed rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(124, 58, 237, 0.4) !important;
    background: rgba(124, 58, 237, 0.02) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(124, 58, 237, 0.2) !important;
    background: rgba(255, 255, 255, 0.05) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 13px !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
}
[data-testid="stMetricValue"] {
    font-size: 26px !important;
    color: #f8fafc !important;
    font-weight: 700 !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    gap: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    margin-bottom: 24px !important;
}
.stTabs [data-baseweb="tab"] {
    height: 44px !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    border-bottom: none !important;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(124, 58, 237, 0.15) !important;
    color: #c084fc !important;
    font-weight: 600 !important;
    border: 1px solid rgba(124, 58, 237, 0.3) !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #f8fafc !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}

/* Heartbeat animation for footer */
@keyframes heartbeat {
    0% { transform: scale(1); }
    12% { transform: scale(1.3); }
    24% { transform: scale(1.1); }
    36% { transform: scale(1.3); }
    60% { transform: scale(1); }
    100% { transform: scale(1); }
}
.heart {
    display: inline-block;
    color: #ef4444 !important;
    animation: heartbeat 1.5s infinite;
    margin: 0 4px;
}

hr {
    border-color: rgba(255, 255, 255, 0.08) !important;
}

/* Custom slider thumb */
div[role="slider"] {
    background-color: #7c3aed !important;
}

/* Loading spinner color matching */
div[data-testid="stSpinner"] > div {
    border-top-color: #7c3aed !important;
}

/* Custom scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.25);
}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
BASE = "https://api.sarvam.ai"

LANG_CODES = {
    "Auto-detect":  "auto",
    "Hindi":        "hi-IN",
    "Bengali":      "bn-IN",
    "Kannada":      "kn-IN",
    "Malayalam":    "ml-IN",
    "Marathi":      "mr-IN",
    "Odia":         "od-IN",
    "Punjabi":      "pa-IN",
    "Tamil":        "ta-IN",
    "Telugu":       "te-IN",
    "Gujarati":     "gu-IN",
    "English":      "en-IN",
}
LANG_LIST = list(LANG_CODES.keys())

# All valid Bulbul v2 speakers from the API error message
TTS_SPEAKERS = [
    "anushka", "abhilash", "manisha", "vidya", "arya", "karun", "hitesh",
    "aditya", "ritu", "priya", "neha", "rahul", "pooja", "rohan", "simran",
    "kavya", "amit", "dev", "ishita", "shreya", "ratan", "varun", "manan",
    "sumit", "roopa", "kabir", "aayan", "shubh", "ashutosh", "advait",
    "anand", "tanya", "tarun", "sunny", "mani", "gokul", "vijay", "shruti",
    "suhani", "mohit", "kavitha", "rehan", "soham", "rupali",
]

def api_headers(key):
    return {"api-subscription-key": key, "Content-Type": "application/json"}

def show_response(label, data, ok=True):
    badge = "badge-ok" if ok else "badge-err"
    icon  = "✅" if ok else "❌"
    text  = json.dumps(data, indent=2, ensure_ascii=False) if isinstance(data, (dict, list)) else str(data)
    st.markdown(f'<span class="{badge}">{icon} {label}</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="response-box">{text}</div>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇮🇳 Sarvam AI Tester")
    st.markdown("---")

    custom = st.text_input("🔑 API Key", value=API_KEY, type="password",
                           help="Loaded from .env · You can override here")
    ACTIVE_KEY = custom.strip() if custom.strip() else API_KEY.strip()

    if ACTIVE_KEY:
        st.markdown('<p class="key-ok">✓ API Key loaded</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="key-err">✗ No API Key — add to .env</p>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
**Available Tests**
- 🌐 Translation
- 🔍 Language Detection
- 🔊 Text-to-Speech
- 🎤 Speech-to-Text
- 📊 API Health
""")
    st.markdown("---")
    st.markdown("📄 [Sarvam Docs](https://docs.sarvam.ai)")
    st.markdown("💬 [Discord](https://discord.com/invite/5rAsykttcs)")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 40px 0 20px">
  <h1 style="font-weight:800; margin:0; font-size:clamp(2.2rem, 5vw, 3rem); line-height:1.2;">🇮🇳 <span style="background: linear-gradient(135deg, #a78bfa, #818cf8, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Sarvam AI API Tester</span></h1>
  <p style="color:#a78bfa; margin-top:10px; font-size:1.1rem; font-weight: 600; letter-spacing: 0.5px;">Built as Open Source for the Community</p>
  <p style="color:#94a3b8; margin-top:12px; font-size:clamp(0.95rem, 2vw, 1.1rem); font-weight: 400; max-width: 650px; margin-left: auto; margin-right: auto; padding: 0 16px; line-height: 1.6;">
    Test India's leading AI models. Seamlessly validate Translation, Language Detection, Text-to-Speech, and Speech-to-Text endpoints with real-time feedback.
  </p>
</div>
""", unsafe_allow_html=True)

if not ACTIVE_KEY:
    st.warning("⚠️  Please add your `SARVAM_API_KEY` to the `.env` file or enter it in the sidebar.")
    st.code("# .env\nSARVAM_API_KEY=your_key_here", language="bash")
    st.stop()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🌐 Translation",
    "🔍 Lang Detect",
    "🔊 Text-to-Speech",
    "🎤 Speech-to-Text",
    "📊 API Health",
])

# ─── 1. Translation ───────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("### 🌐 Text Translation")
    #

    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox("Source Language", LANG_LIST, index=0, key="tr_src")
    with col2:
        tgt_opts = [l for l in LANG_LIST if l != "Auto-detect"]
        tgt_lang = st.selectbox("Target Language", tgt_opts,
                                index=tgt_opts.index("Hindi"), key="tr_tgt")

    tr_text = st.text_area("Text to Translate",
                           value="Hello! How are you doing today?", height=120, key="tr_in")
    gender  = st.selectbox("Speaker Gender", ["Male", "Female"], key="tr_gender")

    if st.button("Translate ➜", key="tr_btn"):
        with st.spinner("Translating…"):
            payload = {
                "input": tr_text,
                "source_language_code": LANG_CODES[src_lang],
                "target_language_code": LANG_CODES[tgt_lang],
                "speaker_gender": gender,
                "mode": "formal",
                "enable_preprocessing": True,
            }
            try:
                r = requests.post(f"{BASE}/translate",
                                  headers=api_headers(ACTIVE_KEY), json=payload, timeout=20)
                data = r.json()
                if r.ok:
                    result = data.get("translated_text", data)
                    st.success("Translation successful!")
                    st.markdown(f"""
                    <div class="card">
                      <p style="color:#94a3b8;font-size:12px;margin:0">Translated ({tgt_lang})</p>
                      <p style="color:#e0e0ff;font-size:1.2rem;margin-top:8px">{result}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("Raw JSON"):
                        show_response("Response", data)
                else:
                    show_response(f"Error {r.status_code}", data, ok=False)
            except Exception as e:
                show_response("Exception", str(e), ok=False)

    #

# ─── 2. Language Detection ────────────────────────────────────────────────────
with tabs[1]:
    st.markdown("### 🔍 Language Identification")
    #

    ld_text = st.text_area("Enter text in any Indian language",
                           value="नमस्ते, आप कैसे हैं? मुझे आपसे मिलकर बहुत खुशी हुई।",
                           height=120, key="ld_in")

    if st.button("Detect Language 🔍", key="ld_btn"):
        with st.spinner("Detecting…"):
            payload = {"input": ld_text}
            try:
                r = requests.post(f"{BASE}/text-lid",
                                  headers=api_headers(ACTIVE_KEY), json=payload, timeout=15)
                data = r.json()
                if r.ok:
                    lang   = data.get("language_code", "unknown")
                    script = data.get("script_code", "")
                    st.success("Language detected!")
                    c1, c2 = st.columns(2)
                    c1.metric("Language Code", lang)
                    c2.metric("Script", script or "—")
                    with st.expander("Raw JSON"):
                        show_response("Response", data)
                else:
                    show_response(f"Error {r.status_code}", data, ok=False)
            except Exception as e:
                show_response("Exception", str(e), ok=False)

    #

# ─── 3. Text-to-Speech ────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown("### 🔊 Text-to-Speech")
    #

    tts_text = st.text_area("Text to Speak",
                            value="नमस्ते! मैं सर्वम AI हूँ। मैं भारतीय भाषाओं में बोल सकता हूँ।",
                            height=100, key="tts_in")

    col1, col2, col3 = st.columns(3)
    with col1:
        tts_lang = st.selectbox("Language",
                                [l for l in LANG_LIST if l != "Auto-detect"],
                                index=0, key="tts_lang")
    with col2:
        tts_spk = st.selectbox("Speaker", TTS_SPEAKERS,
                               index=TTS_SPEAKERS.index("anushka"), key="tts_spk")
    with col3:
        tts_pace = st.slider("Pace", 0.5, 2.0, 1.0, 0.1, key="tts_pace")

    if st.button("Generate Audio 🔊", key="tts_btn"):
        with st.spinner("Synthesizing speech…"):
            payload = {
                "inputs": [tts_text],
                "target_language_code": LANG_CODES[tts_lang],
                "speaker": tts_spk,
                "pitch": 0,
                "pace": tts_pace,
                "loudness": 1.5,
                "speech_sample_rate": 22050,
                "enable_preprocessing": True,
                "model": "bulbul:v2",
            }
            try:
                r = requests.post(f"{BASE}/text-to-speech",
                                  headers=api_headers(ACTIVE_KEY), json=payload, timeout=30)
                data = r.json()
                if r.ok:
                    audio_b64 = data.get("audios", [None])[0]
                    if audio_b64:
                        audio_bytes = base64.b64decode(audio_b64)
                        st.success("Audio generated!")
                        st.audio(audio_bytes, format="audio/wav")
                        st.download_button("⬇️ Download WAV", audio_bytes,
                                           file_name="sarvam_tts.wav", mime="audio/wav")
                    else:
                        show_response("No audio in response", data, ok=False)
                    with st.expander("Raw JSON (audio truncated)"):
                        preview = {k: (v[:80] + "…" if isinstance(v, str) and len(v) > 80 else v)
                                   for k, v in data.items()}
                        show_response("Response", preview)
                else:
                    show_response(f"Error {r.status_code}", data, ok=False)
            except Exception as e:
                show_response("Exception", str(e), ok=False)

    st.markdown("---")
    with st.expander("🎙️ Available Speakers (44 voices)"):
        cols = st.columns(6)
        for i, spk in enumerate(TTS_SPEAKERS):
            cols[i % 6].markdown(f"• {spk}")

    #

# ─── 4. Speech-to-Text ────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown("### 🎤 Speech-to-Text")
    #

    uploaded = st.file_uploader("Upload audio file (WAV/MP3/OGG, ≤ 30 sec)",
                                type=["wav", "mp3", "ogg", "flac", "m4a"], key="stt_file")
    col1, col2 = st.columns(2)
    with col1:
        stt_model = st.selectbox("Model", ["saaras:v3", "saarika:v2"], key="stt_model")
    with col2:
        stt_mode  = st.selectbox("Output Mode",
                                 ["transcribe", "translate", "verbatim", "translit", "codemix"],
                                 key="stt_mode")

    if uploaded and st.button("Transcribe 🎤", key="stt_btn"):
        with st.spinner("Transcribing…"):
            try:
                file_bytes = uploaded.read()
                files   = {"file": (uploaded.name, file_bytes, uploaded.type)}
                payload = {"model": stt_model, "mode": stt_mode}
                r = requests.post(
                    f"{BASE}/speech-to-text",
                    headers={"api-subscription-key": ACTIVE_KEY},
                    files=files, data=payload, timeout=60,
                )
                data = r.json()
                if r.ok:
                    transcript = data.get("transcript",
                                 data.get("transliterated_text", str(data)))
                    st.success("Transcription complete!")
                    st.markdown(f"""
                    <div class="card">
                      <p style="color:#94a3b8;font-size:12px;margin:0">📝 Transcript ({stt_mode})</p>
                      <p style="color:#e0e0ff;font-size:1.1rem;margin-top:8px">{transcript}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("Raw JSON"):
                        show_response("Response", data)
                else:
                    show_response(f"Error {r.status_code}", data, ok=False)
            except Exception as e:
                show_response("Exception", str(e), ok=False)
    elif not uploaded:
        st.info("📂 Upload an audio file above to test STT.")

    #

# ─── 5. API Health ────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown("### 📊 API Health Check")
    st.markdown("Quickly ping all endpoints to verify your API key works.")
    #

    if st.button("🚀 Run Health Check on All Endpoints", key="health_btn"):
        endpoints = [
            ("Translation",    f"{BASE}/translate",
             {"input": "Hello", "source_language_code": "en-IN",
              "target_language_code": "hi-IN", "speaker_gender": "Male"}),
            ("Lang Detection", f"{BASE}/text-lid",
             {"input": "नमस्ते"}),
            ("Text-to-Speech", f"{BASE}/text-to-speech",
             {"inputs": ["नमस्ते"], "target_language_code": "hi-IN",
              "speaker": "anushka", "model": "bulbul:v2"}),
            ("Speech-to-Text", f"{BASE}/speech-to-text",
             {"model": "saaras:v3", "mode": "transcribe"}),
        ]

        results  = []
        progress = st.progress(0)
        status   = st.empty()

        for i, (name, url, body) in enumerate(endpoints):
            status.info(f"Testing {name}…")
            try:
                if name == "Speech-to-Text":
                    dummy_wav = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
                    files = {"file": ("dummy.wav", dummy_wav, "audio/wav")}
                    r = requests.post(
                        url,
                        headers={"api-subscription-key": ACTIVE_KEY},
                        files=files, data=body, timeout=25
                    )
                else:
                    r = requests.post(url, headers=api_headers(ACTIVE_KEY),
                                      json=body, timeout=20)
                results.append((name, r.ok, r.status_code, r.elapsed.total_seconds()))
            except Exception as e:
                results.append((name, False, "ERR", 0.0))
            progress.progress((i + 1) / len(endpoints))

        status.empty()
        progress.empty()

        st.markdown("#### Results")
        cols = st.columns(len(results))
        for col, (name, ok, code, elapsed) in zip(cols, results):
            icon = "✅" if ok else "❌"
            col.markdown(f"""
            <div class="card" style="text-align:center">
              <p style="font-size:2rem;margin:0">{icon}</p>
              <p style="font-weight:600;margin:4px 0;color:#e0e0ff">{name}</p>
              <p style="color:#94a3b8;font-size:12px">HTTP {code}</p>
              <p style="color:#94a3b8;font-size:12px">{elapsed:.2f}s</p>
            </div>
            """, unsafe_allow_html=True)

        all_ok = all(ok for _, ok, _, _ in results)
        if all_ok:
            st.success("🎉 All endpoints healthy! Your API key is working correctly.")
        else:
            failed = [n for n, ok, _, _ in results if not ok]
            st.error(f"⚠️ Issues with: {', '.join(failed)}. Check your API key or quota.")

    #

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 30px 0 20px; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 40px;">
  <p style="color:#94a3b8; font-size:14px; margin: 0 0 8px 0;">
    Sarvam AI API Tester ·
    <a href="https://docs.sarvam.ai" style="color:#a78bfa; text-decoration:none;">Docs</a> ·
    <a href="https://dashboard.sarvam.ai" style="color:#a78bfa; text-decoration:none;">Dashboard</a>
  </p>
  <p style="color:#64748b; font-size:13px; margin:0; font-family:'Inter', sans-serif;">
    Made by <span class="heart">♥</span> by Ravi Panchal. All Rights Reservered @2026.
  </p>
</div>
""", unsafe_allow_html=True)