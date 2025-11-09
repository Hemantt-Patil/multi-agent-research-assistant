
import os
import aiohttp
import json

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class CriticAgent:
    """
    Reviews summary and cross-checks against the original snippets.
    Returns an annotated/validated version of the summary (can include notes).
    """

    async def validate(self, summary: str, sources: list):
        prompt = (
            "You are a careful fact-checker. Given the summary below and the original "
            "short source snippets, identify any statements that look uncertain or "
            "unsupported. For each such statement, add a short note in brackets indicating "
            "the potential issue, and at the end provide a accuracy score (0-100).\n\n"
            f"SUMMARY:\n{summary}\n\nSOURCES:\n"
        )

        for i, s in enumerate(sources[:6], 1):
            prompt += f"\n[{i}] {s}\n"

        prompt += "\nReturn the annotated summary followed by a one-line 'SCORE: <number>'"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "mixtral-8x7b",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 600,
            "temperature": 0.0,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(GROQ_API_URL, json=payload, headers=headers, timeout=30) as resp:
                res = await resp.json()
                try:
                    content = res["choices"][0]["message"]["content"]
                except Exception:
                    content = "ERROR_CRITIC: " + json.dumps(res)
                return content
