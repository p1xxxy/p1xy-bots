from dotenv import load_dotenv

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not configured."
        " Please check your .env file."
    )
    
ADMIN_ID_RAW = os.getenv("ADMIN_ID")
if not ADMIN_ID_RAW:
    raise RuntimeError(
        "ADMIN_ID is not configured."
        " Please check your .env file."
    )
try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except ValueError:
    raise RuntimeError(
        "ADMIN_ID is not a valid integer."
        " Please check your .env file."
    )