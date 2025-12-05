"""
fileinfo_schema.py — Задание 4 (версия без внешних библиотек)

1. Класс FileInfo – хранит сведения о файле.
2. Сбор информации о файлах из data/processed/
3. Сериализация в JSON → output/fileinfo_data.json
4. Создание JSON Schema → output/fileinfo_schema.json
5. Ручная валидация JSON по JSON Schema (проверяем типы и обязательные поля).
"""

from pathlib import Path
import json
import logging
from datetime import datetime


ROOT = Path(__file__).parent
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "output"
LOG = ROOT / "logs" / "app.log"


logging.basicConfig(
    filename=LOG,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


# === 1. Класс FileInfo ===
class FileInfo:
    def __init__(self, path: Path):
        self.file_name = path.name
        self.full_path = str(path.resolve())
        self.size = path.stat().st_size
        self.created = datetime.fromtimestamp(path.stat().st_ctime).isoformat()
        self.modified = datetime.fromtimestamp(path.stat().st_mtime).isoformat()

    def to_dict(self) -> dict:
        """Преобразование объекта в словарь (для JSON)."""
        return {
            "file_name": self.file_name,
            "full_path": self.full_path,
            "size": self.size,
            "created": self.created,
            "modified": self.modified,
        }


# === 2. Сбор информации о processed-файлах ===
def collect_file_info() -> Path:
    OUTPUT.mkdir(exist_ok=True)
    files_info = []

    for f in PROCESSED.glob("*"):
        if f.is_file():
            info = FileInfo(f)
            files_info.append(info.to_dict())
            logging.info(f"📄 Добавлен в JSON: {f.name}")

    json_path = OUTPUT / "fileinfo_data.json"
    json_path.write_text(
        json.dumps(files_info, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"✔ fileinfo_data.json создан → {json_path}")
    return json_path


# === 3. Создание JSON Schema ===
def create_schema() -> Path:
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string"},
                "full_path": {"type": "string"},
                "size": {"type": "number"},
                "created": {"type": "string"},
                "modified": {"type": "string"},
            },
            "required": ["file_name", "full_path", "size", "modified"],
        },
    }

    schema_path = OUTPUT / "fileinfo_schema.json"
    schema_path.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"✔ fileinfo_schema.json создан → {schema_path}")
    return schema_path


# === 4. Ручная валидация JSON по JSON Schema ===
def validate(json_file: Path, schema_file: Path) -> None:
    data = json.loads(Path(json_file).read_text(encoding="utf-8"))
    schema = json.loads(Path(schema_file).read_text(encoding="utf-8"))

    errors: list[str] = []

    # 4.1. Проверяем тип корня
    if schema.get("type") != "array":
        errors.append("Схема ожидает, что корневой элемент — массив (type='array').")

    if not isinstance(data, list):
        errors.append("JSON-документ должен быть списком объектов.")

    # Если корень уже не список — дальше нет смысла, но пойдём мягко
    item_schema = schema.get("items", {})
    props = item_schema.get("properties", {})
    required = item_schema.get("required", [])

    # 4.2. Проверяем каждый элемент массива
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"[{idx}] Элемент массива должен быть объектом (dict).")
            continue

        # обязательные поля
        for field in required:
            if field not in item:
                errors.append(f"[{idx}] Отсутствует обязательное поле '{field}'.")

        # проверка типов по свойствам
        for name, value in item.items():
            if name not in props:
                # поле не описано в схеме — можно проигнорировать или предупредить
                continue

            expected_type = props[name].get("type")

            if expected_type == "string" and not isinstance(value, str):
                errors.append(
                    f"[{idx}] Поле '{name}' должно быть строкой, а получен тип {type(value).__name__}."
                )
            if expected_type == "number" and not isinstance(value, (int, float)):
                errors.append(
                    f"[{idx}] Поле '{name}' должно быть числом, а получен тип {type(value).__name__}."
                )

    # 4.3. Результат
    if not errors:
        print(" JSON полностью валиден по заданной JSON Schema!")
        logging.info("JSON fileinfo_data.json прошёл валидацию по JSON Schema.")
    else:
        print(" Обнаружены ошибки валидации JSON:")
        for err in errors:
            print("  -", err)
        logging.error("Ошибки валидации JSON: " + "; ".join(errors))


if __name__ == "__main__":
    json_path = collect_file_info()
    schema_path = create_schema()
    validate(json_path, schema_path)

