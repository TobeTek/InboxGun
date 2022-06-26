#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r ./requirements.txt

# python ./mysite/manage.py collectstatic --no-input
python ./mysite/manage.py migrate

python ./mysite/manage.py createsuperuser --no-input --username testmaster --email testmaster@email.com

ls -la ./mysite 

echo "Done with Build!"

