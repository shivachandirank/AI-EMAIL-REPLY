import os
import base64
import pickle
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

app = Flask(__name__, static_folder="frontend")
CORS(app)

# ================= CONFIG =================
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

CLIENT_SECRETS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"

# 🔐 IMPORTANT: use env variable (recommended)
GROK_API_KEY = os.getenv("") or "YOUR_API_KEY_HERE"

# ================= GMAIL =================
def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    if not creds or not creds.valid:
        return None

    return build("gmail", "v1", credentials=creds)


# ================= ROUTES =================
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")


# ================= AUTH =================
@app.route("/auth/login")
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:5000/auth/callback",
    )

    auth_url, _ = flow.authorization_url(prompt="consent")
    return jsonify({"auth_url": auth_url})


@app.route("/auth/callback")
def callback():
    code = request.args.get("code")

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri="http://127.0.0.1:5000/auth/callback",
    )

    flow.fetch_token(code=code)

    with open(TOKEN_FILE, "wb") as f:
        pickle.dump(flow.credentials, f)

    return """
    <script>
      window.opener.postMessage('auth_success', '*');
      window.close();
    </script>
    """


@app.route("/auth/status")
def status():
    service = get_gmail_service()
    if service:
        profile = service.users().getProfile(userId="me").execute()
        return jsonify({"authenticated": True, "email": profile["emailAddress"]})
    return jsonify({"authenticated": False})


@app.route("/auth/logout")
def logout():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
    return jsonify({"success": True})


# ================= EMAIL =================
@app.route("/emails")
def emails():
    service = get_gmail_service()
    if not service:
        return jsonify({"error": "Not authenticated"}), 401

    msgs = service.users().messages().list(userId="me", maxResults=20).execute()
    messages = msgs.get("messages", [])

    email_list = []

    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"]).execute()
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}

        email_list.append({
            "id": m["id"],
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "snippet": msg.get("snippet", "")
        })

    return jsonify({"emails": email_list})


@app.route("/emails/<id>")
def get_email(id):
    service = get_gmail_service()
    msg = service.users().messages().get(userId="me", id=id).execute()

    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}

    body = ""
    parts = msg["payload"].get("parts", [])
    if parts:
        data = parts[0]["body"].get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data).decode()

    return jsonify({
        "id": id,
        "from": headers.get("From", ""),
        "subject": headers.get("Subject", ""),
        "body": body
    })


# ================= GROK AI (FIXED) =================
@app.route("/generate-reply", methods=["POST"])
def generate_reply():
    try:
        data = request.json

        prompt = f"""
Write a professional email reply.

Subject: {data.get('email_subject')}
From: {data.get('email_from')}
Body: {data.get('email_body')}

Tone: {data.get('tone')}
Intent: {data.get('intent')}

End with:
Best regards,
{data.get('sender_name')}
"""

        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-beta",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        # 🔥 DEBUG
        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        result = response.json()

        # ✅ SAFE PARSING (FIXED)
        reply = ""

        if "choices" in result:
            if len(result["choices"]) > 0:
                reply = result["choices"][0].get("message", {}).get("content", "")

        # fallback if structure different
        if not reply:
            reply = result.get("message", "")

        # final fallback
        if not reply:
            reply = str(result)

        return jsonify({"result": f"REPLY:\n{reply}"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"result": f"REPLY:\nError: {str(e)}"})


# ================= SEND =================
@app.route("/send-reply", methods=["POST"])
def send_reply():
    service = get_gmail_service()

    data = request.json

    msg = MIMEText(data.get("body"))
    msg["to"] = data.get("to")
    msg["subject"] = "Re: " + data.get("subject")

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    return jsonify({"success": True})


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)