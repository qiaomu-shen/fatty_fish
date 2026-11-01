"""读取配置；密钥不会放入源码或 dataclass 的调试文本表示。"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    root: Path
    database_path: Path
    api_key: str = field(repr=False)
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-v4-pro"


def load_settings() -> Settings:
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root / ".env", override=False)
    database_path = Path(os.getenv("CHATBOT_DB_PATH", "data/chat.db"))
    if not database_path.is_absolute():
        database_path = root / database_path
    return Settings(
        root=root,
        database_path=database_path,
        api_key=os.getenv("DEEPSEEK_API_KEY", "").strip(),
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/"),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro"),
    )
