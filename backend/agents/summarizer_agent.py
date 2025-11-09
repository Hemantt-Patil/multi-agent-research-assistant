# backend/agents/summarizer_agent.py
import os
import aiohttp
import json

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class SummarizerAgent:
    """Calls Groq (chat style) to summarize a list of textual sources."""

    async def summarize(self, sources: list, topic: str):
        if not sources:
            return "No sources to summarize."

        prompt = (
            f"You are an expert research summarizer. Produce a concise, factual summary "
            f"of the following findings about the topic: '{topic}'.\n\n"
            f"Sources:\n"
        )
        # include up to 6 sources with separators
        for i, s in enumerate(sources[:6], 1):
            prompt += f"\n[{i}] {s}\n"

        prompt += (
            "\nReturn a clear multi-paragraph summary (2-6 paragraphs). "
            "Avoid hallucination and say when information is uncertain.\n"
        )

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "mixtral-8x7b",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
            "temperature": 0.2,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(GROQ_API_URL, json=payload, headers=headers, timeout=30) as resp:
                res = await resp.json()
                # defensive checks
                try:
                    content = res["choices"][0]["message"]["content"]
                except Exception:
                    # return the raw response for easier debugging
                    content = "ERROR_SUMMARIZER: " + json.dumps(res)
                return content
