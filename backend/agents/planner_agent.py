# backend/agents/planner_agent.py
import os
import aiohttp
import json

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class PlannerAgent:
    """
    Planner Agent:
    Generates a detailed markdown research report using validated or annotated summaries.
    """

    async def compile(self, topic: str, validated_summary: str):
        if not GROQ_API_KEY:
            return "❌ ERROR: Missing GROQ_API_KEY environment variable."

        prompt = (
            "You are an expert AI research planner and technical writer. "
            "Using the validated annotated summary below, produce a structured markdown research report "
            "for engineers and decision-makers. Include the following sections:\n\n"
            "1. **Title**\n"
            "2. **TL;DR** (2-3 concise sentences)\n"
            "3. **Key Findings** (bullet list)\n"
            "4. **Detailed Discussion** (3-5 paragraphs)\n"
            "5. **Reference Notes** (short citation-style list)\n\n"
            f"TOPIC: {topic}\n\n"
            f"VALIDATED SUMMARY:\n{validated_summary}\n\n"
            "Make the report professional, data-driven, and clear. Use proper markdown formatting."
        )

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "llama-3.3-70b-versatile",  # updated to a supported model
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1200,
            "temperature": 0.2,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(GROQ_API_URL, json=payload, headers=headers, timeout=60) as resp:
                    res = await resp.json()
                    if "choices" in res and len(res["choices"]) > 0:
                        return res["choices"][0]["message"]["content"]
                    else:
                        return "ERROR_PLANNER_RESPONSE: " + json.dumps(res)
        except Exception as e:
            return f"ERROR_PLANNER_EXCEPTION: {str(e)}"
