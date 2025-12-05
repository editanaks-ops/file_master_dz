"""
main.py — скрипт для Задания 1.

Создаёт структуру каталогов проекта:
project_root/
├── data/
│   ├── raw/
│   ├── processed/
├── logs/
├── backups/
└── output/

+ создаёт несколько текстовых файлов с разными кодировками в data/raw
+ пишет лог в logs/app.log о выполненных действиях
"""

from pathlib import Path
import logging


# Определяем корень проекта как папку, где лежит этот файл main.py
PROJECT_ROOT = Path(__file__).parent

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
LOGS_DIR = PROJECT_ROOT / "logs"
BACKUPS_DIR = PROJECT_ROOT / "backups"
OUTPUT_DIR = PROJECT_ROOT / "output"

LOG_FILE = LOGS_DIR / "app.log"


def setup_logging():
    """Настраиваем логирование в файл logs/app.log."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    logging.info("=== Запуск скрипта main.py (Задание 1) ===")


def create_directories():
    """Создаёт все нужные директории, если их ещё нет."""
    for directory in [DATA_DIR, RAW_DIR, PROCESSED_DIR, LOGS_DIR, BACKUPS_DIR, OUTPUT_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        logging.info(f"Проверена/создана директория: {directory}")


def create_sample_raw_files():
    """
    Создаём несколько текстовых файлов в разных кодировках в data/raw/.

    file_utf8.txt   — UTF-8, русский/английский текст
    file_latin1.txt — ISO-8859-1, латинский текст
    file_cp1251.txt — cp1251, русский текст (старая Windows-кодировка)
    """
    # 1. UTF-8
    utf8_file = RAW_DIR / "file_utf8.txt"
    utf8_content = "Привет, мир! Hello world! Это файл в кодировке UTF-8."
    utf8_file.write_text(utf8_content, encoding="utf-8")
    logging.info(f"Создан файл (UTF-8): {utf8_file}")

    # 2. ISO-8859-1 (latin-1)
    latin1_file = RAW_DIR / "file_latin1.txt"
    latin1_content = "Bonjour le monde! Ola mundo! ÆØÅ — пример символов latin-1."
    # кириллица в этой кодировке не поддерживается, поэтому только латиница
    latin1_file.write_text(latin1_content, encoding="iso-8859-1", errors="ignore")
    logging.info(f"Создан файл (ISO-8859-1): {latin1_file}")

    # 3. cp1251 — классическая русская Windows-кодировка
    cp1251_file = RAW_DIR / "file_cp1251.txt"
    cp1251_content = "Это пример файла в кодировке cp1251. Старые добрые времена Windows :)"
    cp1251_file.write_text(cp1251_content, encoding="cp1251")
    logging.info(f"Создан файл (cp1251): {cp1251_file}")


def main():
    setup_logging()
    create_directories()
    create_sample_raw_files()
    logging.info("Структура проекта и примерные файлы созданы успешно.")
    print(" Структура проекта создана, примеры файлов записаны.")
    print("Проверь папку проекта и файл logs/app.log для подробностей.")


if __name__ == "__main__":
    main()
