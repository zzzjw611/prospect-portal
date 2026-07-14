from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.config import get_settings
from app.database import initialize_database


def main() -> None:
    settings = get_settings()
    initialize_database(settings)
    print(f"Database migrated at {settings.database_path}")


if __name__ == "__main__":
    main()
