"""
restore_backup.py — Задание 3 (восстановление)

Разархивирует последний созданный архив в папку restored_data/
"""


from pathlib import Path
import zipfile
import logging


ROOT = Path(__file__).parent
BACKUPS = ROOT / "backups"
RESTORE_DIR = ROOT / "restored_data"
LOG_FILE = ROOT / "logs" / "app.log"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def restore_backup():
    # Сортируем архивы по времени, берём самый свежий
    archives = sorted(BACKUPS.glob("*.zip"))
    if not archives:
        print(" Нет архивов для восстановления.")
        return

    last_backup = archives[-1]  # последний = самый новый

    RESTORE_DIR.mkdir(exist_ok=True)

    with zipfile.ZipFile(last_backup, "r") as zip_ref:
        zip_ref.extractall(RESTORE_DIR)

    logging.info(f" Архив восстановлен: {last_backup.name}")
    print(f"\nФайлы восстановлены из → {last_backup.name}")
    print(f"Папка восстановления → {RESTORE_DIR}")


if __name__ == "__main__":
    restore_backup()
