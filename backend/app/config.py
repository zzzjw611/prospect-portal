from functools import lru_cache
from pathlib import Path
import os


def _load_env_file() -> None:
    env_path = Path(".env")
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


class Settings:
    app_env: str
    database_path: Path
    storage_dir: Path
    internal_api_token: str
    attorney_email: str
    cors_origins: list[str]
    smtp_host: str | None
    smtp_port: int
    smtp_username: str | None
    smtp_password: str | None
    smtp_from_email: str
    smtp_use_tls: bool
    max_resume_bytes: int

    def __init__(self) -> None:
        _load_env_file()
        self.app_env = os.getenv("APP_ENV", "development")
        self.database_path = Path(os.getenv("DATABASE_PATH", "app.db"))
        self.storage_dir = Path(os.getenv("STORAGE_DIR", "storage"))
        self.internal_api_token = os.getenv("INTERNAL_API_TOKEN", "dev-attorney-token")
        self.attorney_email = os.getenv("ATTORNEY_EMAIL", "attorney@example.com")
        self.cors_origins = [
            origin.strip()
            for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
            if origin.strip()
        ]
        self.smtp_host = os.getenv("SMTP_HOST") or None
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME") or None
        self.smtp_password = os.getenv("SMTP_PASSWORD") or None
        self.smtp_from_email = os.getenv("SMTP_FROM_EMAIL", "no-reply@example.com")
        self.smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
        self.max_resume_bytes = int(os.getenv("MAX_RESUME_BYTES", str(10 * 1024 * 1024)))


@lru_cache
def get_settings() -> Settings:
    return Settings()
