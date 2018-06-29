release: apt-get update
release: python neo_cities/manage.py makemigrations
release: python neo_cities/manage.py migrate
web: python neo_cities/manage.py runserver 0.0.0.0:$PORT
