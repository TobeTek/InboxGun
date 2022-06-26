#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r ./requirements.txt

cd mysite

python ./mysite/manage.py collectstatic --no-input
python ./mysite/manage.py migrate

echo "Done with Build!"

