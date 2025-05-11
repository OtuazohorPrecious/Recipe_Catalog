# Create new file build.sh in project root
#!/usr/bin/env bash
set -o errexit

poetry install
python manage.py migrate
python manage.py collectstatic --noinput