# 🤖 AI Sheets Manager – Intelligent Google Sheets Dashboard

A premium, state-of-the-art full-stack implementation that transforms a simple Google Sheet into an intelligent database managed by an Open-Source LLM. Built with **FastAPI**, **LangChain**, and **Groq (Llama 3.1)**.

![Dashboard Preview](https://via.placeholder.com/1200x600.png?text=AI+Sheets+Manager+Dashboard)

---

## 🌟 Key Features

- 🧠 **AI-Powered Management**: Talk to your spreadsheet in natural language. Ask to "Update John's score" or "Remove duplicates".
- 🛠 **Autonomous Tool Calling**: The LLM uses specialized tools to Read, Search, Add, Update, and Delete data in real-time.
- 🎨 **Premium Glassmorphism UI**: A stunning, modern dashboard with animated backgrounds and sleek interactive elements.
- 🔐 **Secure Google OAuth 2.0**: Enterprise-grade authentication for Google Sheets API.
- ⚡ **Lightning Fast**: Powered by Groq's Llama 3.1 for near-instant AI responses.
- 🧹 **Smart Cleanup**: AI-driven duplicate removal and data normalization.

---

## 🛠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | FastAPI (Python) |
| **LLM Orchestration** | LangChain |
| **Model** | Groq (Llama 3.1 8B Instant) |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript |
| **Cloud Integration** | Google Sheets API v4 |
| **Authentication** | Google OAuth 2.0 (token-based) |

---

## 📂 Project Structure

```text
.
├── app.py                # Core FastAPI application & AI Agent logic
├── .env                  # Environment secrets (API Keys, etc.)
├── client_secret.json    # Google Cloud OAuth credentials
├── requirements.txt      # Project dependencies
├── templates/
│   └── index.html        # Premium AI Dashboard
└── README.md             # You are here!
```

---

## ⚙️ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Ananjay07/AI-Sheets-Manager.git
cd AI-Sheets-Manager
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Google Cloud
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Enable **Google Sheets API**.
3. Create **OAuth 2.0 Client ID (Desktop App)**.
4. Download the JSON, rename it to `client_secret.json`, and place it in the root.

### 4️⃣ Configure Environment
Create a `.env` file in the root:
```env
GROQ_API_KEY=your_groq_api_key_here
SPREADSHEET_ID=your_google_sheet_id_here
```

### 5️⃣ Run the Application
```bash
python -m uvicorn app:app --reload --port 8001
```
Visit `http://127.0.0.1:8001` to start managing your data with AI.

---

## 🗣 AI Interaction Examples

- *"Add a new user named Alice with email alice@example.com and score 95."*
- *"Search for any users with 'X' in their name."*
- *"Clean up the sheet – remove all duplicate entries."*
- *"Update the score of the user with email john@gmail.com to 88."*

---

## 🎨 Design Philosophy

Sheet Intelligence uses a **Future-Tech** aesthetic:
- **Aura backgrounds**: Dynamic, moving aura effects for a living UI.
- **Glassmorphism**: Translucent cards with subtle borders and heavy background blurs.
- **Micro-animations**: Smooth transitions for AI chat bubbles and data table updates.

---

## ⭐ Support
If you love this project, give it a ⭐ on GitHub!

