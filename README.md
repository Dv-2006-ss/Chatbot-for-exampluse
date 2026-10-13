# Kreeti Computers - ExamPulse AI Chatbot

An AI-powered help assistant for **Kreeti Computers** and its online examination portal **ExamPulse**. Built with FastAPI, Groq LLM API, Tailwind CSS, and Alpine.js.

---

## Features

- **Course & Exam Assistance**: Answers queries regarding institute courses (Python, C, C++, MS Office, Tally ERP 9, Digital Marketing, Video Editing, Graphic Design) and ExamPulse rules.
- **Rule-Based Fallbacks & Roasts**: Instant responses for common questions and lighthearted roast responses for course duration queries.
- **Lightweight & Fast**: Single-page frontend using Tailwind CSS and Alpine.js, backed by a FastAPI backend.
- **Session Management**: Tracks the conversation history per session with instant reset option.

---

## Tech Stack

- **Backend**: Python 3.10+, [FastAPI](https://fastapi.tiangolo.com/), [Groq Python SDK](https://github.com/groq/groq-python), `python-dotenv`, `uvicorn`
- **Frontend**: HTML5, [Tailwind CSS](https://tailwindcss.com/) (CDN), [Alpine.js](https://alpinejs.dev/) (CDN)

---

## Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- A [Groq API Key](https://console.groq.com/keys)

### 2. Setup Environment

Clone the repository and navigate into the project directory:
```bash
git clone https://github.com/Dv-2006-ss/Chatbot-for-exampluse.git
cd Chatbot-for-exampluse
```

Install the dependencies:
```bash
pip install fastapi uvicorn groq python-dotenv
```

### 3. Environment Variables

Copy `.env.example` to `.env` and provide your Groq API key:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the Server

Start the application with Uvicorn:
```bash
uvicorn main:app --reload
```

Open your browser and navigate to:
```
http://127.0.0.1:8000
```
