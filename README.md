# 🚀 AI Email Reply Generator (Gmail + Grok API)

An intelligent email assistant that reads your Gmail inbox and generates smart, context-aware replies using AI.

---

## 📌 Features

- 🔐 Google OAuth Authentication (Secure Gmail Access)
- 📥 Read Emails from Gmail Inbox
- 🤖 AI-Powered Reply Generation (Grok API)
- ✏️ Refine Replies (Shorter, Formal, Friendly, etc.)
- 📤 Send Replies Directly via Gmail
- ⚡ Real-time UI with Clean UX
- 🔄 Auto Email Analysis (Intent, Tone, Summary)

---

## 🛠️ Tech Stack

| Layer      | Technology                    |
|------------|-------------------------------|
| Frontend   | HTML, CSS, JavaScript         |
| Backend    | Python, Flask                 |
| AI Model   | Grok API (xAI)                |
| APIs       | Gmail API (Google Cloud)      |

---

## 📂 Project Structure

roject/ ├── app.py ├── credentials.json ├── token.pickle ├── requirements.txt └── frontend/ └── index.html


---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ai-email-reply.git
cd ai-email-reply
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Setup Environment Variables
Create a .env file:

GROK_API_KEY=your_grok_api_key_here
4️⃣ Setup Google OAuth
Go to Google Cloud Console
Enable Gmail API
Create OAuth credentials
Download credentials.json
Place it in the project root
5️⃣ Run the Application
python app.py
Open in browser: http://127.0.0.1:5000

🔑 API Integration
Grok API (xAI)
Used for generating AI-powered replies
Endpoint: https://api.x.ai/v1/chat/completions
🧠 How It Works
User logs in via Gmail OAuth
App fetches emails using Gmail API
User selects an email
AI generates a reply using Grok
User can refine or send the reply
📸 Screenshots (Optional)
Add screenshots of your UI here.

🚀 Future Enhancements
🔥 Auto-reply system for incoming emails
📊 Email analytics dashboard
🌐 Deploy on cloud (Render/AWS)
🧩 Chrome Extension
🤝 Contributing
Feel free to fork this repo and submit pull requests.

📜 License
This project is open-source and available under the MIT License.

👨‍💻 Author
SIVACHANDIRAN K

⭐ If you like this project, give it a star!
