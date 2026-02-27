from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as GoogleRequest

import os
import pickle

# ================== CONFIG ==================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1aY-ERNLMzPOM8t9KiJJsL-6ztAVzIfM4txfJIpnJ-uI"
RANGE_NAME = "Sheet1!A:C"
# ============================================

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# ========== GOOGLE AUTH FUNCTION ==========
def authenticate_google():
    creds = None

    # Load existing token
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials → login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


# Authenticate once at startup
creds = authenticate_google()
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()


# ========== FRONTEND ROUTES ==========

@app.get("/", response_class=HTMLResponse)
def home(request: Request, success: bool = False):
    return templates.TemplateResponse("index.html", {"request": request, "success": success})


@app.post("/submit")
def submit(
    name: str = Form(...),
    email: str = Form(...),
    score: int = Form(...)
):
    values = [[name, email, score]]
    body = {"values": values}

    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

    return RedirectResponse(url="/?success=true", status_code=303)


# ========== OPTIONAL API ROUTES ==========

class User(BaseModel):
    name: str
    email: str
    score: int


@app.post("/api/add-user/")
def add_user(user: User):
    values = [[user.name, user.email, user.score]]
    body = {"values": values}

    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()

    return {"message": "User added successfully!"}


@app.get("/api/get-users/")
def get_users():
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()

    rows = result.get("values", [])
    return {"data": rows}

