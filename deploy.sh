cd ./mysite
python ./manage.py runserver 0.0.0.0
# gunicorn mysite.asgi:application