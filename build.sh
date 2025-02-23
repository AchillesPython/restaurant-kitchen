#!/bin/bash

# Встановлення залежностей
pip install -r requirements.txt

# Виконання міграцій
python manage.py migrate --noinput

# Збір статичних файлів
python manage.py collectstatic --noinput

# ОБОВ'ЯЗКОВЕ створення суперкористувача (навіть якщо він існує)
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
"

# Запуск Gunicorn
gunicorn kitchen_service.wsgi:application
