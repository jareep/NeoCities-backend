release: apt-get update;apt-get install docker-ce;docker run -p 6379:6379 -d redis:2.8
release: python neo_cities/manage.py makemigrations
release: python neo_cities/manage.py migrate
web: python neo_cities/manage.py runserver 0.0.0.0:$PORT
