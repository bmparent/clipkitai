"""Scrape trending keywords from Etsy and Creative Fabrica RSS feeds into Redis."""
import os, time
import feedparser
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(REDIS_URL, decode_responses=True)

RSS_FEEDS = {
    "etsy": "https://www.etsy.com/trends/feed",
    "cf": "https://www.creativefabrica.com/trending/feed/"
}

def fetch_keywords(limit: int = 200) -> list[str]:
    """Return up to *limit* lower‑cased terms from both feeds."""
    terms: set[str] = set()
    for url in RSS_FEEDS.values():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            terms.add(entry.title.lower())
    return list(terms)[:limit]

def push_keywords(keywords: list[str]) -> None:
    """Insert keywords into a sorted‑set `ckai:keywords` with the current timestamp."""
    now = int(time.time())
    pipe = r.pipeline()
    for kw in keywords:
        pipe.zadd("ckai:keywords", {kw: now})
    pipe.execute()

if __name__ == "__main__":
    kws = fetch_keywords()
    push_keywords(kws)
    print(f"Pushed {len(kws)} keywords to Redis.")
