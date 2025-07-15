"""Generate 5 PNGs (2048×2048) for one keyword using HuggingFace SDXL."""
import os, time, pathlib, requests
from io import BytesIO
from PIL import Image
import redis
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(REDIS_URL, decode_responses=True)

ASSET_ROOT = pathlib.Path("assets")
ASSET_ROOT.mkdir(exist_ok=True)

def pop_keyword() -> str | None:
    res = r.zpopmin("ckai:keywords", 1)
    return res[0][0] if res else None

def slugify(text: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in text).lower()[:40]

def generate_image(prompt: str) -> bytes:
    resp = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    resp.raise_for_status()
    return resp.content

def main() -> None:
    kw = pop_keyword()
    if not kw:
        print("No keywords left in Redis.")
        return

    slug = slugify(kw)
    out_dir = ASSET_ROOT / slug
    out_dir.mkdir(exist_ok=True)

    for i in range(5):
        img_bytes = generate_image(kw)
        img = Image.open(BytesIO(img_bytes))
        img.save(out_dir / f"{slug}_{i+1}.png")
        time.sleep(1)  # HuggingFace rate‑limit buffer

    print(f"Generated pack '{slug}' → {out_dir}")

if __name__ == "__main__":
    main()
