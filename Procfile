release: python manage.py migrate
web: daphne django_chat.asgi:application --port $POST --bind 0.0.0.0 -v2

