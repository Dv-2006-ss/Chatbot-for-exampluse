import os, random
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq

# Load environment variables and initialize
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Warning: GROQ_API_KEY is missing in .env file!")

app = FastAPI()
client = Groq(api_key=api_key)
chat_history = {}  # Store last 10 messages per session
SYSTEM_PROMPT = """You are the help assistant for Kreeti Computers, a computer training institute.
- Courses: Python, C, C++, MS Office, Tally ERP 9, Digital Marketing, Video Editing, Graphic Design.
- Students take exams and assignments on ExamPulse, the institute's online exam portal. Each exam allows one attempt, is timed, runs in fullscreen, and students cannot go back to previous questions. Leaving fullscreen or switching tabs gives a warning and the 3rd violation auto-submits. After submitting, the student confirms their name and gets a certificate. Accounts and passwords are managed by the Admin.
Rules:
- Answer questions about Kreeti Computers (the institute, its courses, the ExamPulse exam portal) AND questions about the content of the subjects it teaches: Python, C, C++, MS Office, Tally ERP 9, Digital Marketing, Video Editing, Graphic Design. Examples: "what is a loop in Python?", "what is a pointer in C?", "what is a ledger in Tally?", "what is SEO?", "how do I use VLOOKUP?".
- Explain like a friendly teacher for a beginner student. Keep it short, with a tiny example when useful.
- If the question is about neither Kreeti Computers nor these subjects (movies, politics, general knowledge), reply with a short light joke saying you only help with Kreeti Computers and its subjects.
- Never invent fees, timings, address, phone numbers or course durations. If unknown, say so and suggest contacting the institute.
- Explain concepts freely, but if someone pastes an exam question and asks for the answer, don't give it directly. Help them understand the concept instead.
- Reply in plain text only. Do not use markdown symbols like **, # or tables. For lists, use simple lines starting with '- '."""

ROASTS = [
    "Python in 7 days? Sure, and I'll become a billionaire by Monday. 😂",
    "It takes as long as you spend practicing, not scrolling reels. 😅",
    "Rome wasn't built in a day, and your coding skills won't be either! 😉",
    "Depends! Daily practice: fast. Only opening your laptop on Sundays: next century! 😜",
    "That totally depends on how many bugs you create along the way! 🐛"
]

FALLBACKS = {
    ("course", "subject", "teach"): "We teach Python, C, C++, MS Office, Tally ERP 9, Digital Marketing, Video Editing, and Graphic Design.",
    ("attempt",): "Each exam on ExamPulse allows only one attempt.",
    ("fullscreen",): "Exams must run in fullscreen. Exiting triggers warnings and can auto-submit.",
    ("tab",): "Switching tabs triggers warnings. On the 3rd violation, the exam auto-submits.",
    ("certificate",): "After exam submission and name confirmation, you receive your certificate.",
    ("password",): "ExamPulse login credentials and passwords are managed by the Admin."
}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.get("/")
def get_home():
    return FileResponse("index.html")

@app.post("/chat")
def handle_chat(req: ChatRequest):
    msg, sid = req.message.strip(), req.session_id
    low = msg.lower()

    # Rule 1: Roast without calling API if asking about duration
    time_words = ["how long", "how much time", "duration", "how many months", "how many weeks", "how many days", "time to learn", "kitna time"]
    if any(w in low for w in time_words):
        return {"reply": f"{random.choice(ROASTS)} Ask Kreeti Computers for the exact duration."}

    # Maintain last 10 messages per session
    history = chat_history.setdefault(sid, [])
    history.append({"role": "user", "content": msg})
    if len(history) > 10:
        history.pop(0)

    # Groq API call with Rule 2 Fallback
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            max_tokens=800
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print(repr(e))
        reply = next((ans for keys, ans in FALLBACKS.items() if any(k in low for k in keys)), "Sorry, the AI service is unavailable right now.")

    history.append({"role": "assistant", "content": reply})
    return {"reply": reply}

@app.delete("/chat/{session_id}")
def reset_chat(session_id: str):
    chat_history.pop(session_id, None)
    return {"status": "cleared"}
