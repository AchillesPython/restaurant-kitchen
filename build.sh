#!/usr/bin/env bash
# Exit on error
set -o errexit

# Встановлення залежностей
pip install -r requirements.txt

# Збір статичних файлів без підтвердження
python manage.py collectstatic --no-input

# Виконання міграцій бази даних
python manage.py migrate --noinput

# Імпорт даних із файлу test_data.json
python manage.py loaddata test_data.json

# Запуск серверу Gunicorn
gunicorn kitchen_service.wsgi:application
