# KaspiBoard

Доска объявлений: веб на **Django** (шаблоны + формы) и **REST API** для мобильного клиента на **Flutter**.

## Требования

- Python 3.10+ (рекомендуется)
- [Flutter SDK](https://docs.flutter.dev/get-started/install) — только для папки `mobile_flutter`

## Запуск бэкенда (Django)

```bash
cd путь/к/проекту
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r req.txt
python manage.py migrate
python manage.py runserver
```

Сайт: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Мобильное приложение (Flutter)

```bash
cd mobile_flutter
flutter pub get
flutter run
```

По умолчанию приложение обращается к API на `http://127.0.0.1:8000` (для Android-эмулятора в коде используется `10.0.2.2`).

## Структура

| Папка / файл | Назначение |
|--------------|------------|
| `ad_project/` | настройки Django |
| `core_app/` | модели, представления, шаблоны, статика |
| `mobile_flutter/` | клиент на Flutter |
| `req.txt` | зависимости Python |

