# 🇮🇳 Sarvam AI API Tester

A beautiful, dark-themed Streamlit dashboard to test the major **Sarvam AI** API endpoints — India's full-stack sovereign AI platform built for Indian languages.

> [!NOTE]
> **Open Source & Forking**: This is an open-source project designed for testing the Sarvam AI API across various use cases. Anyone is free to fork this repository, customize the code, and use it for their own testing or applications.

---

## 📋 Table of Contents

- [What is Sarvam AI?](#what-is-sarvam-ai)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [How to Get Your API Key](#how-to-get-your-api-key)
- [Running the App](#running-the-app)
- [Feature Guide](#feature-guide)
- [Troubleshooting](#troubleshooting)
- [Forking & Open Source](#forking--open-source)
- [Useful Links](#useful-links)

---

## What is Sarvam AI?

[Sarvam AI](https://www.sarvam.ai) is an Indian AI company that builds language models and APIs specifically designed for India's 22+ languages. It provides:

- **Speech-to-Text** (STT) — Transcribe spoken Indian language audio
- **Text-to-Speech** (TTS) — Generate natural-sounding Indian voice audio
- **Translation** — Translate text between 10+ Indian languages
- **Language Detection** — Identify which Indian language a piece of text is in
- **Chat Completion** — Converse with Sarvam's LLMs in Indic languages

This tester app lets you call each of these APIs directly from a clean UI without writing any code.

---

## Features

| Tab | API Endpoint | What It Does |
|-----|-------------|--------------|
| 🌐 **Translation** | `/translate` | Translates text between Hindi, Bengali, Tamil, Telugu, Gujarati, and 6 more Indian languages |
| 🔍 **Lang Detect** | `/text-lid` | Detects which Indian language a block of text is written in |
| 🔊 **Text-to-Speech** | `/text-to-speech` | Converts text into natural audio using Bulbul v2 (44 voices) |
| 🎤 **Speech-to-Text** | `/speech-to-text` | Transcribes an uploaded audio file using Saaras v3 |
| 📊 **API Health** | All of the above | Pings all endpoints at once to verify your API key and quota |

---

## Project Structure

```
sarvam_tester/
├── app.py              ← Main Streamlit application
├── .env                ← Your API key goes here (never commit this!)
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
└── test_inputs.txt     ← Ready-to-use test inputs for each feature
```

---

## Prerequisites

- Python **3.8 or higher**
- pip (Python package manager)
- A Sarvam AI account and API key (free to start)

---

## Setup & Installation

### Step 1 — Clone or download the project

If you downloaded the zip:
```bash
unzip sarvam_tester.zip
cd sarvam_tester
```

### Step 2 — Create a virtual environment (recommended)

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — The web UI framework
- `sarvamai` — Official Sarvam AI Python SDK
- `python-dotenv` — Loads your API key from the `.env` file
- `requests` — Makes HTTP calls to the Sarvam API

### Step 4 — Add your API key

Open the `.env` file and replace the placeholder:

```env
SARVAM_API_KEY=your_actual_key_here
```

> ⚠️ Never share or commit your `.env` file. It contains your private API key.

---

## How to Get Your API Key

1. Go to [dashboard.sarvam.ai](https://dashboard.sarvam.ai)
2. Sign up for a free account
3. Navigate to **API Keys** in the sidebar
4. Click **Create New Key**
5. Copy the key and paste it into your `.env` file

Free tier includes enough credits to test all features comfortably.

---

## Running the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at:
```
http://localhost:8501
```

You can also override the API key directly in the sidebar text box inside the app — useful if you want to test a different key without editing `.env`.

---

## Feature Guide

### 🌐 Translation

Translates text from one Indian language to another.

- **Source Language** — The language your input text is written in. Select "Auto-detect" if unsure.
- **Target Language** — The language you want the output in.
- **Speaker Gender** — Affects some language-specific grammar (Male / Female).
- **Supported Languages** — Hindi, Bengali, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu, Gujarati, English.

---

### 🔍 Language Detection

Paste any text written in an Indian language and the API will identify it.

- Returns a **language code** (e.g., `hi-IN` for Hindi, `ta-IN` for Tamil)
- Also returns the **script code** (e.g., `Deva` for Devanagari, `Taml` for Tamil script)
- Supports all major Indian scripts

---

### 🔊 Text-to-Speech

Converts text into a playable audio clip using Sarvam's **Bulbul v2** model.

- **Language** — The language of the text you're converting
- **Speaker** — Choose from **44 available voices** (anushka, abhilash, manisha, vidya, arya, karun, hitesh, aditya, ritu, priya, neha, rahul, pooja, rohan, simran, kavya, amit, dev, ishita, shreya, ratan, varun, manan, sumit, roopa, kabir, aayan, shubh, ashutosh, advait, anand, tanya, tarun, sunny, mani, gokul, vijay, shruti, suhani, mohit, kavitha, rehan, soham, rupali)
- **Pace** — Speed of speech from 0.5x (slow) to 2.0x (fast). Default is 1.0.
- After generation, you can **play the audio inline** or **download it as a WAV file**
- Text limit: up to **2500 characters** per request

---

### 🎤 Speech-to-Text

Upload an audio file and get back a text transcription.

- **Supported formats** — WAV, MP3, OGG, FLAC, M4A
- **Max duration** — 30 seconds per file (use Batch API for longer audio)
- **Model** — Saaras v3 (recommended) or Saarika v2 (legacy)
- **Output Modes:**
  | Mode | Description |
  |------|-------------|
  | `transcribe` | Transcribes audio in the original spoken language |
  | `translate` | Transcribes and translates audio to English |
  | `verbatim` | Word-for-word transcription without normalization |
  | `translit` | Romanizes the Indian language text (e.g., Hindi → "namaste") |
  | `codemix` | Mixes scripts intelligently for code-switched speech |

---

### 📊 API Health Check

Pings the Translation, Language Detection, and Text-to-Speech endpoints in sequence and shows:
- ✅ / ❌ status for each endpoint
- HTTP status code returned
- Response latency in seconds

Use this first to confirm your API key is valid and your account has credits.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `No API Key` shown in sidebar | Check your `.env` file has `SARVAM_API_KEY=...` with no extra spaces |
| `401 Unauthorized` | Your API key is wrong or expired — regenerate it at the dashboard |
| `429 Too Many Requests` | You've hit your rate limit — wait a moment and retry |
| Speaker not recognized error | Use only speakers from the 44 valid list shown in the TTS tab |
| Audio not playing | Try downloading the WAV and opening it locally |
| STT gives empty transcript | Ensure the audio is clear, under 30 seconds, and in a supported format |
| App won't start | Run `pip install -r requirements.txt` again inside your virtual environment |

---

## 🍴 Forking & Open Source

This repository is a fully **open-source project** intended to simplify testing, playing, and experimenting with the Sarvam AI API in different scenarios (Translation, Lang Detect, TTS, STT, and health checking). 

### 🚀 How to Fork and Use
1. Click the **Fork** button at the top right of this repository's GitHub page.
2. Clone your forked repository to your local machine.
3. Follow the [Setup & Installation](#setup--installation) instructions.
4. Customize the Streamlit UI, add more endpoints, or integrate it into your own pipelines!

Feel free to open issues or submit pull requests with improvements!

---

## Useful Links

- 🌐 [Sarvam AI Website](https://www.sarvam.ai)
- 📄 [API Documentation](https://docs.sarvam.ai)
- 🎛️ [Dashboard & API Keys](https://dashboard.sarvam.ai)
- 🧪 [API Playground](https://dashboard.sarvam.ai/playground)
- 💬 [Discord Community](https://discord.com/invite/5rAsykttcs)
- 📦 [Sarvam Python SDK](https://pypi.org/project/sarvamai/)