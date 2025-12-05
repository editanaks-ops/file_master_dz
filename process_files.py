"""
process_files.py — Задание 2

1) читает файлы из data/raw/, определяет кодировку;
2) меняет регистр текста на противоположный (swapcase);
3) сохраняет новые файлы в data/processed/;
4) создаёт JSON с деталями о каждом обработанном файле.
"""

from pathlib import Path
import json
from datetime import datetime
import logging


# Пути проекта
ROOT = Path(__file__).parent
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
OUTPUT = ROOT / "output"
LOG_FILE = ROOT / "logs" / "app.log"


# Логирование
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def read_with_encoding(file_path: Path):
    """Пытаемся прочитать файл тремя кодировками — простое автоопределение."""
    encodings = ["utf-8", "cp1251", "iso-8859-1"]
    for enc in encodings:
        try:
            text = file_path.read_text(encoding=enc)
            return text, enc
        except Exception:
            continue
    raise ValueError(f"❌ Кодировка не определена: {file_path}")


def process_files():
    """Основная обработка файлов."""
    OUTPUT.mkdir(exist_ok=True)
    PROC.mkdir(exist_ok=True)

    result = []

    for file in RAW.glob("*"):
        if file.is_file():
            raw_text, encoding = read_with_encoding(file)

            processed_text = raw_text.swapcase()  # Меняем регистр

            new_name = f"{file.stem}_processed{file.suffix}"
            new_path = PROC / new_name
            new_path.write_text(processed_text, encoding="utf-8")

            size = new_path.stat().st_size
            modified = datetime.fromtimestamp(new_path.stat().st_mtime).isoformat()

            data = {
                "file_name": new_name,
                "encoding_used": encoding,
                "original_text": raw_text,
                "processed_text": processed_text,
                "file_size_bytes": size,
                "last_modified": modified
            }

            result.append(data)

            logging.info(f"✔ Обработан файл {file.name} → {new_name}")

    json_path = OUTPUT / "processed_data.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n Готово! Файлы обработаны.")
    print(f"JSON создан → {json_path}")


if __name__ == "__main__":
    process_files()
