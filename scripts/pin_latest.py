"""Pin the newest generated thumbnail to Pinterest via API v5."""
import os, pathlib, random, requests, sys
from dotenv import load_dotenv

load_dotenv()
PIN_TOKEN = os.getenv("PIN_KEY")                # required
BOARD_ID  = os.getenv("PIN_BOARD_ID", "")       # optional specific board
ASSETS    = pathlib.Path("assets")
API_URL   = "https://api.pinterest.com/v5/pins"
HDRS      = {"Authorization": f"Bearer {PIN_TOKEN}"}

if not PIN_TOKEN:
    sys.exit("PIN_KEY is not set; skipping pin step.")

def newest_thumb() -> pathlib.Path:
    packs = sorted(ASSETS.glob("*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for pack in packs:
        thumbs = list(pack.glob("*.png"))
        if thumbs:
            return random.choice(thumbs)
    raise FileNotFoundError("No thumbnails found under assets/.")

def post_pin(img: pathlib.Path):
    data = {"title": img.parent.name.replace("_", " ").title()}
    if BOARD_ID:
        data["board_id"] = BOARD_ID
    files = {"media": img.open("rb")}
    r = requests.post(API_URL, headers=HDRS, data=data, files=files, timeout=60)
    r.raise_for_status()
    print("📌  Pinned:", r.json().get("id"))

if __name__ == "__main__":
    try:
        post_pin(newest_thumb())
    except Exception as e:
        print("Pinterest pin failed:", e, file=sys.stderr)
        sys.exit(0)  # don\u2019t break the workflow
