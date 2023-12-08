#!/bin/bash

# Apply database migrations
#sleep 600
#echo "Copy executers on /usr/bin/"
#for FILE in optimization/built/scripts/executer/*; do
#	if [ -f "$FILE" ]; then
#		echo "$FILE"
#		chmod +x "$FILE"
#		cp "$FILE" /usr/bin/
#	fi
#done
#
#echo "Copy executers on /usr/bin/"
#for FILE in optimization/built/scripts/services/*; do
#	if [ -f "$FILE" ]; then
#		echo "$FILE"
#		cp "$FILE" /etc/systemd/system/
#		systemctl enable "${FILE##*/}"
#		systemctl start "${FILE##*/}" 
#	fi
#done
systemctl --type=service --state=running
#celery -A api4opt beat --loglevel=info --detach
#celery -A api4opt worker --loglevel=info
#python manage.py runserver 0.0.0.0:8000
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

echo "Create superuser"
python manage.py createsuperuser --noinput --first_name $DJANGO_SUPERUSER_FIRST_NAME --last_name $DJANGO_SUPERUSER_LAST_NAME --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000

