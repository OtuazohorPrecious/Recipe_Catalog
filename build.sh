# Create new file build.sh in project root
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py makemigrations
python manage.py collectstatic --noinput