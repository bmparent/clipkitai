"""Zip each generated pack and upload to Payhip."""
import os, pathlib, zipfile, requests, time
from dotenv import load_dotenv

load_dotenv()

PAYHIP_TOKEN = os.getenv("PAYHIP_TOKEN")
PAYHIP_API = "https://payhip.com/api/v2/products"
HEADERS = {"Authorization": f"Bearer {PAYHIP_TOKEN}"}

ASSET_ROOT = pathlib.Path("assets")

def make_zip(folder: pathlib.Path) -> pathlib.Path:
    zip_path = folder.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for img in folder.glob("*.png"):
            zf.write(img, img.name)
        zf.writestr("license.txt", "Royalty-free for personal and commercial use.")
    return zip_path

def upload(zip_path: pathlib.Path, title: str, price_cents: int = 300) -> str:
    data = {
        "product[price]": str(price_cents),
        "product[title]": title,
    }
    files = {"file": zip_path.open("rb")}
    resp = requests.post(PAYHIP_API, headers=HEADERS, data=data, files=files)
    if resp.status_code == 429:
        time.sleep(5)
        return upload(zip_path, title, price_cents)
    resp.raise_for_status()
    return resp.json()["permalink"]

def main() -> None:
    for pack_dir in ASSET_ROOT.iterdir():
        if pack_dir.is_dir():
            zip_path = make_zip(pack_dir)
            permalink = upload(zip_path, pack_dir.name.replace("_", " ").title())
            print("Uploaded →", permalink)

if __name__ == "__main__":
    main()
