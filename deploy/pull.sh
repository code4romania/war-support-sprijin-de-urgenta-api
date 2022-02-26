set -e

cd /root/centre_testare_HIV
git reset --hard HEAD
git pull

docker-compose build --build-arg ENVIRONMENT=development db cache api
docker-compose up -d db cache api
