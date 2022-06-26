cd ./mysite
# python ./manage.py runserver 0.0.0.0
uvicorn mysite.asgi:application 
# gunicorn mysite.asgi:application