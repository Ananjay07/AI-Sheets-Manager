# 🚀 FastSheets – Premium FastAPI + Google Sheets Integration

A high-performance, visually stunning web application built with **FastAPI**, **Google OAuth 2.0**, and **Google Sheets API**. FastSheets allows you to submit data through a modern, vibrant landing page and sync it instantly with your cloud spreadsheets.

---

## 🌟 Key Features

- ⚡ **High-Performance Backend**: Powered by FastAPI for lightning-fast request handling.
- 🎨 **Vibrant UI**: A modern 'Vibrant Sunset' design with glassmorphism and mesh gradients.
- 🔐 **Secure Auth**: Fully integrated with Google OAuth 2.0 for secure data access.
- 📊 **Cloud Sync**: Real-time data appending to Google Sheets without manual entry.
- 🔔 **Success Feedback**: Polished toast notifications for a premium user experience.
- 📱 **Fully Responsive**: Optimized for desktop, tablet, and mobile viewing.

---

## 🛠 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | FastAPI (Python) |
| **Frontend** | HTML5, CSS3 (Vanilla), Jinja2 |
| **Auth** | Google OAuth 2.0 |
| **Storage** | Google Sheets API v4 |
| **Server** | Uvicorn |

---

## 📂 Project Structure

```text
01_fastsheets-api-main/
│
├── app.py                # FastAPI Backend & OAuth Logic
├── client_secret.json    # Your Google Cloud Credentials
├── requirements.txt      # Python Dependencies
├── templates/
│   └── index.html        # Premium 'Vibrant Sunset' Frontend
└── README.md             # Project Documentation
```

---

## ⚙️ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/fastsheets-api.git
cd fastsheets-api
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Google Cloud (Required)
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable **Google Sheets API**.
4. Configure **OAuth Consent Screen** (Add your email as a test user).
5. Create **OAuth 2.0 Client ID (Desktop App)**.
6. Download the JSON, rename it to `client_secret.json`, and place it in the root directory.

### 4️⃣ Configure your Spreadsheet
1. Create a new Google Sheet.
2. Copy the **Spreadsheet ID** from the URL: `https://docs.google.com/spreadsheets/d/YOUR_ID_HERE/edit`.
3. Update `SPREADSHEET_ID` in `app.py` ([line 15](app.py#L15)).

### 5️⃣ Run the Application
```bash
python -m uvicorn app:app --reload
```
Open `http://127.0.0.1:8000` in your browser.

---

## 🎨 Design Philosophy

FastSheets moves away from generic administrative UIs. It uses a **"Vibrant Sunset"** aesthetic:
- **Aura Backgrounds**: Animated radial gradients for a dynamic feel.
- **Crystal Glassmorphism**: Cards use heavy blur and subtle borders to feel premium.
- **Typography**: Uses 'Outfit' for a clean, modern, and readable tech look.

---

## 👩‍💻 Author
Developed with ❤️ by **Namradha Mani**.

---

## ⭐ Support
If you find this project useful, give it a ⭐ on GitHub!
