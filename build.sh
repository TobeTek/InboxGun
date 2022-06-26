#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r ./requirements.txt

python ./mysite/manage.py collectstatic --no-input
python ./mysite/manage.py migrate

# Create a superuser
python ./mysite/manage.py createsuperuser --no-input --username testmaster --email testmaster@email.com

# Create some dummy blog posts
python ./mysite/manage.py gen_articles_data --n 20
python ./mysite/manage.py load_articles

ls -la ./mysite 

echo "Done with Build!"

