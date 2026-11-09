from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "sleepinsight.db"

class Config:
    DATABASE_URL = os.getenv("SLEEPINSIGHT_DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")
    JSON_SORT_KEYS = False
    SECRET_KEY = os.getenv("SLEEPINSIGHT_SECRET_KEY", "development-only-change-me")
