# release: python manage.py makemigrations && python3 manage.py migrate
web: daphne django_chat.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer -v2