import aiohttp
import asyncio
from utils.helper import safe_text

class ResearcherAgent:
    """
    Simple researcher that queries DuckDuckGo Instant Answer API and returns
    short text snippets. In production replace with SERP API or managed scraper.
    """

    DDG_URL = "https://api.duckduckgo.com/"

    async def fetch_ddg(self, session, q):
        params = {"q": q, "format": "json", "no_redirect": 1, "skip_disambig": 1}
        async with session.get(self.DDG_URL, params=params, timeout=15) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            return data

    async def search(self, topic: str, max_results: int = 6):
        # build a few query variants
        queries = [
            topic,
            f"{topic} latest trends",
            f"{topic} research summary",
            f"{topic} overview"
        ]

        results = []
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_ddg(session, q) for q in queries]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            for r in responses:
                if isinstance(r, dict):
                    # extract RelatedTopics text snippets
                    related = r.get("RelatedTopics", [])
                    for item in related:
                        text = item.get("Text") or item.get("Result") or None
                        if text:
                            cleaned = safe_text(text)
                            results.append(cleaned)
                            if len(results) >= max_results:
                                break
                if len(results) >= max_results:
                    break

        # fallback if nothing found
        if not results:
            results = [f"No direct DDG hits found for '{topic}'. Provide more context."]

        return results
