docker ps -a|grep -v CONTAINER| awk {'print $1'}|xargs docker stop
docker ps -a|grep -v CONTAINER| awk {'print $1'}|xargs docker rm
sudo docker-compose -f docker-compose.prod.yml up -d --build
sudo docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
sudo docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
docker ps -a

