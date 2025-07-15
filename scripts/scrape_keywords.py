"""Fetch trending keyword titles from RSS feeds and push them to Redis."""
import os
import time
import requests
import feedparser
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(REDIS_URL, decode_responses=True)

RSS_FEEDS = {
    "etsy": "https://www.etsy.com/trends/feed",
    "cf": "https://www.creativefabrica.com/trending/feed/",
}

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0 Safari/537.36"
)

FALLBACK = [
    "kawaii icons",
    "pastel clipart",
    "rocket sticker",
    "watercolor flower",
    "minimal ui icons",
]


def fetch_keywords(limit: int = 200) -> list[str]:
    """Return up to *limit* unique titles from all feeds."""
    headers = {"User-Agent": UA}
    seen: set[str] = set()
    out: list[str] = []
    for url in RSS_FEEDS.values():
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue
        feed = feedparser.parse(resp.text)
        for entry in getattr(feed, "entries", []):
            title = getattr(entry, "title", "").strip().lower()
            if title and title not in seen:
                seen.add(title)
                out.append(title)
                if len(out) >= limit:
                    break
        if len(out) >= limit:
            break
    if not out:
        out = FALLBACK.copy()
    return out[:limit]


def push_keywords(keywords: list[str]) -> None:
    """Push terms into Redis sorted set `ckai:keywords`."""
    now = int(time.time())
    pipe = r.pipeline()
    for kw in keywords:
        pipe.zadd("ckai:keywords", {kw: now})
    pipe.execute()


if __name__ == "__main__":
    kws = fetch_keywords()
    push_keywords(kws)
    print(f"Pushed {len(kws)} keywords to Redis.")
