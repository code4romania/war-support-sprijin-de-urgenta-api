set -e

cd /root/rvm-api-django
git reset --hard HEAD
git pull

docker-compose build --build-arg ENVIRONMENT=development db revm
docker-compose up -d db revm
