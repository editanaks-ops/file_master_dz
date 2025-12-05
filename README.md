#  File Master — Project for working with files, encodings, JSON, backups

  
Работа с файловой системой, сериализацией данных, резервным копированием и JSON Schema валидацией.

##  Функционал

- автоматическое создание структуры проекта
- создание файлов в разных кодировках
- чтение + определение кодировки
- преобразование текста (swapcase)
- сериализация обработанных файлов в JSON
- сбор информации о файлах с помощью класса `FileInfo`
- создание JSON Schema и ручная валидация
- создание zip-резервной копии
- восстановление копии из архива
- генерация итогового отчёта

##  Скрипты

| Файл | Назначение |
|---|---|
| `main.py` | создание структуры проекта + тестовые файлы |
| `process_files.py` | обработка raw файлов → processed + JSON |
| `backup_data.py` | backup → zip |
| `restore_backup.py` | restore из backup |
| `fileinfo_schema.py` | FileInfo + JSON Schema + ручная validation |
| `generate_report.py` | формирование итогового отчёта |

##  Итоговый отчёт

`output/report.txt`  


##  Запуск

```bash
python main.py
python process_files.py
python backup_data.py
python restore_backup.py
python fileinfo_schema.py
python generate_report.py
