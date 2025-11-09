# 🤖 Multi-Agent Research Assistant

A next-gen research assistant powered by multiple intelligent agents — **Researcher, Critic, Summarizer, and Planner** — collaborating to analyze topics and produce structured research reports.

---

## 🧩 Tech Stack
| Layer | Technology |
|--------|-------------|
| **Frontend** | Next.js (TypeScript, Tailwind) |
| **Backend** | FastAPI (Python 3.12.6) |
| **Agents** | Async multi-agent architecture |
| **API Calls** | Groq API or OpenAI-compatible models |

---

## ⚙️ Backend Setup
```bash ```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

## Frontend Setup
cd frontend
npm install
npm run dev
