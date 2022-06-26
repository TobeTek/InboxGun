cd ./mysite
python ./manage.py runserver
# gunicorn mysite.asgi:application