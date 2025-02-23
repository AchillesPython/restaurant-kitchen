#!/bin/bash

# Встановлення залежностей
pip install -r requirements.txt

# Виконання міграцій
python manage.py migrate --noinput

# Збір статичних файлів
python manage.py collectstatic --noinput

# Створення суперкористувача (тільки якщо він не існує)
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='user').exists():
    User.objects.create_superuser('user', 'admin@example.com', 'admin12345')
"

# Запуск Gunicorn
gunicorn kitchen_service.wsgi:application
