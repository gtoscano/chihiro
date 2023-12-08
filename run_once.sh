#rabbitmq-plugins enable rabbitmq_management
#rabbitmqctl add_user "${RABBITMQ_DEFAULT_USER}" "${RABBITMQ_DEFAULT_PASS}"
#rabbitmqctl set_permissions -p / "${RABBITMQ_DEFAULT_USER}" ".*" ".*" ".*"

#rabbitmqctl add_user "${AMQP_USERNAME}" "${AMQP_PASSWORD}"
#rabbitmqctl set_permissions -p / "${AMQP_USERNAME}" ".*" ".*" ".*"



#echo "In create DB"
#mysql -e "CREATE DATABASE ${DB_NAME} /*\!40100 DEFAULT CHARACTER SET utf8 */;"
#mysql -e "CREATE USER ${DB_USER}@localhost IDENTIFIED BY '${DB_PASSWD}';"
#mysql -e "GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';"
#mysql -e "FLUSH PRIVILEGES;"

echo "Apply database migrations"
python manage.py migrate

echo "Create superuser"
python manage.py createsuperuser --noinput --first_name Peter --last_name Parker --email $DJANGO_SUPERUSER_EMAIL

