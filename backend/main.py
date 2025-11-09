# backend/main.py
import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agents.researcher_agent import ResearcherAgent
from agents.summarizer_agent import SummarizerAgent
from agents.critic_agent import CriticAgent
from agents.planner_agent import PlannerAgent
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

app = FastAPI(title="Multi-Agent Research Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    app.extra["groq_missing"] = True
else:
    app.extra["groq_missing"] = False


class TopicRequest(BaseModel):
    topic: str


@app.post("/research")
async def research_topic(request: TopicRequest):
    if app.extra.get("groq_missing"):
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not set in environment.")

    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required.")

    try:
        # instantiate agents (they may use GROQ env internally)
        researcher = ResearcherAgent()
        summarizer = SummarizerAgent()
        critic = CriticAgent()
        planner = PlannerAgent()

        # Step 1 - research
        sources = await researcher.search(topic)

        # Step 2 - summarize
        summary = await summarizer.summarize(sources, topic)

        # Step 3 - critic validates / annotates
        validated = await critic.validate(summary, sources)

        # Step 4 - planner compiles final markdown report
        report = await planner.compile(topic, validated)

        return {"topic": topic, "report": report, "sources_count": len(sources)}
    except Exception as e:
        # provide readable error for dev; in production reduce verbosity
        raise HTTPException(status_code=500, detail=str(e))
