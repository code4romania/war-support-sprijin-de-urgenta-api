help:                             ## Display a help message detailing commands and their purpose
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""

build:                            ## builds the container
	docker-compose build --pull
	docker-compose up -d

build-dev:                        ## builds the container with the development flag
	docker-compose build --build-arg ENVIRONMENT=development --pull
	docker-compose up -d

superuser:                        ## creates a superuser for the API
	docker-compose exec revm ./manage.py createsuperuser

drop-db:                          ## drops the database
	docker-compose down -t 60
	docker volume rm revm-pgdata

## [UTILS]
requirements-build:               ## run pip compile and add requirements from the *.in files
	docker-compose run --rm --no-deps --entrypoint "bash -c" revm "cd /code && pip-compile -o requirements.txt requirements.in && pip-compile -o requirements-dev.txt requirements-dev.in"

requirements-update:              ## run pip compile and rebuild the requirements files
	docker-compose run --rm --no-deps --entrypoint "bash -c" revm "cd /code && pip-compile -r -U -o requirements.txt requirements.in && pip-compile -r -U -o requirements-dev.txt requirements-dev.in && chmod a+r requirements.txt && chmod a+r requirements-dev.txt"

migrations:                       ## generate migrations in a clean container
	docker-compose exec revm ./manage.py makemigrations

migrate:                          ## apply migrations in a clean container
	docker-compose exec revm ./manage.py migrate

makemessages:                     ## generate the strings marked for translation
	docker-compose exec revm ./manage.py makemessages -a

compilemessages:                  ## compile the translations
	docker-compose exec revm ./manage.py compilemessages

collectstatic:
	docker-compose exec revm ./manage.py collectstatic --no-input

format:
	black --line-length=120 --target-version=py39  --exclude migrations ./revm

format-check:
	black --line-length=120 --target-version=py39 --check --diff  --exclude migrations ./revm
