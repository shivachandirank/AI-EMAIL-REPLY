# AI Email Reply Generator — Gemini Edition — Setup Guide

## Project Structure
```
gmail-ai-reply/
├── app.py              ← Flask backend (powered by Gemini)
├── requirements.txt    ← Python dependencies
├── credentials.json    ← (you create this — see Step 2)
├── token.pickle        ← (auto-created after first Gmail login)
└── frontend/
    └── index.html      ← Full UI
```

---

## Step 1 — Install Python dependencies

```bash
cd gmail-ai-reply
pip install -r requirements.txt
```

---

## Step 2 — Get your Gmail API credentials (one-time setup)

1. Go to https://console.cloud.google.com/
2. Create a new project (e.g. "AI Email Reply")
3. Go to **APIs & Services → Enable APIs**
   - Search and enable: **Gmail API**
4. Go to **APIs & Services → OAuth consent screen**
   - Choose "External", fill in App name, save
   - Add your Gmail address as a test user
5. Go to **APIs & Services → Credentials**
   - Click "Create Credentials → OAuth 2.0 Client ID"
   - Application type: **Web application**
   - Authorized redirect URIs: `http://localhost:5000/auth/callback`
   - Click Create
6. Download the JSON → rename it to `credentials.json`
7. Place `credentials.json` in the `gmail-ai-reply/` folder

---

## Step 3 — Get your Gemini API key

1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API key"
3. Copy your key

Then set it as an environment variable:

```bash
# Mac / Linux
export GEMINI_API_KEY="AIza-your-key-here"

# Windows CMD
set GEMINI_API_KEY=AIza-your-key-here

# Windows PowerShell
$env:GEMINI_API_KEY="AIza-your-key-here"
```

---

## Step 4 — Run the server

```bash
python app.py
```

Open your browser: http://localhost:5000

---

## Step 5 — Connect Gmail

1. Click **"Connect Gmail"** in the app banner
2. A Google login popup appears — sign in and grant permissions
3. Your inbox loads automatically

---

## AI Model Used

This project uses **Gemini 2.0 Flash** — Google's fast, capable model.
You can change the model in `app.py` line:

```python
gemini_model = genai.GenerativeModel("gemini-2.0-flash")
```

Other options:
- `gemini-1.5-pro`       — more powerful, slower
- `gemini-1.5-flash`     — fast and efficient
- `gemini-2.0-flash`     — latest fast model (default)

---

## Features

- Reads real Gmail inbox (Inbox, Unread, Sent, Important)
- Click any email to read the full body
- Gemini AI analyzes: email type, urgency, sentiment, key ask
- Generates a smart professional reply with your chosen tone & intent
- One-click refinements: shorter, more formal, warmer, add detail
- Send the reply directly via Gmail with one click

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `redirect_uri_mismatch` | Add `http://localhost:5000/auth/callback` in Google Console |
| `Access blocked` | Add your email as a test user in OAuth consent screen |
| `GEMINI_API_KEY` error | Make sure the env variable is set before running `python app.py` |
| Port already in use | Change `port=5000` in `app.py` to e.g. `5001` |
| `google-generativeai` import error | Run `pip install google-generativeai` again |
