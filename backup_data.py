"""
backup_data.py — Задание 3 (часть 1)

Создаёт ZIP архив резервной копии папки data/
Файл сохраняется в backups/ как backup_YYYYMMDD.zip
"""

from pathlib import Path
import shutil
from datetime import datetime
import logging


ROOT = Path(__file__).parent
DATA = ROOT / "data"
BACKUPS = ROOT / "backups"
LOG = ROOT / "logs" / "app.log"


logging.basicConfig(
    filename=LOG,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def create_backup():
    BACKUPS.mkdir(exist_ok=True)

    date = datetime.now().strftime("%Y%m%d")  # YYYYMMDD
    archive_name = BACKUPS / f"backup_{date}"

    shutil.make_archive(
        base_name=str(archive_name),
        format="zip",
        root_dir=str(DATA)
    )

    logging.info(f" Создан архив: {archive_name}.zip")
    print(f"\nГотово! Архив создан → {archive_name}.zip")


if __name__ == "__main__":
    create_backup()
