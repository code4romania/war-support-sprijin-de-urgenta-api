set -e

cd /home/ec2-user/war-support-sprijin-de-urgenta-api
git reset --hard HEAD
git pull

docker-compose build --build-arg ENVIRONMENT=development db revm
docker-compose up -d db revm
