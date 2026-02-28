from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as GoogleRequest

import os
import pickle
import json
import traceback
from dotenv import load_dotenv


# LangChain Imports for LLM and Tools
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# ================== CONFIG ==================
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "1aY-ERNLMzPOM8t9KiJJsL-6ztAVzIfM4txfJIpnJ-uI")
RANGE_NAME = "Sheet1!A:C"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    print(f"DEBUG: GROQ_API_KEY found (starts with {GROQ_API_KEY[:4]}...)", flush=True)
else:
    print("DEBUG: GROQ_API_KEY NOT FOUND", flush=True)
# ============================================


app = FastAPI()
templates = Jinja2Templates(directory="templates")


# ========== GOOGLE AUTH FUNCTION ==========
def authenticate_google():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


# Authenticate once at startup
creds = authenticate_google()
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()


# ========== LLM TOOLS (Google Sheets Actions) ==========

@tool
def get_all_users():
    """Fetches all users, their emails, and scores from the spreadsheet."""
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()
    rows = result.get("values", [])
    return rows

@tool
def add_user_to_sheet(name: str, email: str, score: int):
    """Adds a new user. If the email already exists, it prompts for an update instead of adding."""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get("values", [])
    
    search_email = email.lower().strip()
    for row in rows:
        if len(row) > 1 and row[1].lower().strip() == search_email:
            return f"Error: A user with email '{email}' already exists. Use 'update_user_score' instead of adding."

    values = [[name, email, score]]
    body = {"values": values}
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()
    return f"Successfully added {name} to the sheet."

@tool
def find_user(query: str):
    """Searches for a user by name or email (case-insensitive). Useful before updating."""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get("values", [])
    
    search_query = query.lower().strip()
    matches = []
    for i, row in enumerate(rows):
        if not row: continue
        # Check Name (row[0]) or Email (row[1])
        name_match = len(row) > 0 and search_query in row[0].lower()
        email_match = len(row) > 1 and search_query in row[1].lower()
        
        if name_match or email_match:
            row_data = {"row_number": i + 1, "data": row}
            matches.append(row_data)
            
    if matches:
        return f"Found matches: {json.dumps(matches)}"
    return f"No users found matching '{query}'."

@tool
def update_user_score(email: str, new_score: int):
    """Updates the score of an existing user identified by their email (case-insensitive)."""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get("values", [])
    
    search_email = email.lower().strip()
    for i, row in enumerate(rows):
        if len(row) > 1 and row[1].lower().strip() == search_email:
            range_to_update = f"Sheet1!C{i+1}"
            body = {"values": [[new_score]]}
            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_to_update,
                valueInputOption="RAW",
                body=body
            ).execute()
            return f"Updated score for {row[1]} (row {i+1}) to {new_score}."
            
    return f"Error: User with email '{email}' not found. Please verify the email in the table."

@tool
def update_user_email(old_email: str, new_email: str):
    """Updates the email address of an existing user identified by their old email."""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get("values", [])
    
    search_email = old_email.lower().strip()
    for i, row in enumerate(rows):
        if len(row) > 1 and row[1].lower().strip() == search_email:
            range_to_update = f"Sheet1!B{i+1}"
            body = {"values": [[new_email]]}
            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_to_update,
                valueInputOption="RAW",
                body=body
            ).execute()
            return f"Updated email for {row[1]} to {new_email}."
            
    return f"Error: User with email '{old_email}' not found."

@tool
def delete_user_by_email(email: str):

    """Deletes a user row from the spreadsheet identified by their email."""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get("values", [])
    
    search_email = email.lower().strip()
    for i, row in enumerate(rows):
        if len(row) > 1 and row[1].lower().strip() == search_email:
            range_to_clear = f"Sheet1!A{i+1}:C{i+1}"
            sheet.values().clear(
                spreadsheetId=SPREADSHEET_ID,
                range=range_to_clear
            ).execute()
            return f"Cleared data for user with email {row[1]}."
            
    return f"Error: User with email '{email}' not found."

@tool
def remove_duplicates():
    """Cleans up the sheet by removing duplicate entries based on email. Keeps the first occurrence."""
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    rows = result.get("values", [])
    
    seen_emails = set()
    rows_to_clear = []
    
    for i, row in enumerate(rows):
        if len(row) > 1:
            email = row[1].lower().strip()
            if email in seen_emails:
                rows_to_clear.append(i + 1)
            else:
                seen_emails.add(email)
                
    if not rows_to_clear:
        return "No duplicates found."
        
    for row_num in reversed(rows_to_clear): 
        range_to_clear = f"Sheet1!A{row_num}:C{row_num}"
        sheet.values().clear(spreadsheetId=SPREADSHEET_ID, range=range_to_clear).execute()
        
    return f"Successfully cleared {len(rows_to_clear)} duplicate rows."

# Initialize LLM and Agent
if GROQ_API_KEY:
    print(f"--- INITIALIZING LLM WITH MODEL: llama-3.1-8b-instant ---", flush=True)
    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=GROQ_API_KEY)
    tools = [get_all_users, find_user, add_user_to_sheet, update_user_score, update_user_email, delete_user_by_email, remove_duplicates]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a specialized Google Sheets manager. "
                   "CRITICAL RULES:\n"
                   "1. ALWAYS use 'find_user' or 'get_all_users' before any action to check if the user exists.\n"
                   "2. DO NOT add a user (add_user_to_sheet) if they already exist in the sheet. "
                   "3. If a user asks to 'change' or 'update' something, and you can't find them, ask for their exact email.\n"
                   "4. Use 'remove_duplicates' if you see duplicate entries in the sheet data.\n"
                   "5. Data structure: [Name, Email, Score]."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
else:
    agent_executor = None


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
    add_user_to_sheet.invoke({"name": name, "email": email, "score": score})
    return RedirectResponse(url="/?success=true", status_code=303)


# ========== API ROUTES ==========

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not GROQ_API_KEY:
        return {"response": "GROQ_API_KEY is missing in your .env file. Please add it to enable the AI."}
    
    if not agent_executor:
        return {"response": "Agent executor not initialized. Check your configuration."}
    
    try:
        print(f"User Query: {request.message}")
        response = agent_executor.invoke({"input": request.message})
        return {"response": response["output"]}
    except Exception as e:
        print("--- AI ERROR ---")
        traceback.print_exc()
        return {"response": f"AI Error: {str(e)}"}


@app.get("/api/get-users/")
def get_users_api():
    try:
        rows = get_all_users.invoke({})
        return {"data": rows}
    except Exception as e:
        return {"data": [], "error": str(e)}



