docker start battlesnakeio.play.pg
docker run -d battlesnakeio/engine
docker run -d battlesnakeio/board

echo "ENV=local; ./play/manage.py runserver"