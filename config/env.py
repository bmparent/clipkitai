"""Environment variable helpers with backwards-compatible names."""
import os

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY") or os.getenv("PAYHIP_TOKEN")
