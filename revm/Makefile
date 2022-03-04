help:                             ## Display a help message detailing commands and their purpose
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""

seed_superuser:                   ## creates a superuser for the API based on the data in the .env file
	./manage.py seed_superuser

seed_groups:                      ## creates initial user groups
	./manage.py seed_groups

superuser: seed_groups seed_superuser

seed_data:                        ## seed categories and subcategories
	./manage.py seed_item_data
	./manage.py seed_transport_service_categories
	./manage.py seed_volunteering_types

seed: seed_groups seed_superuser seed_data    ## create a superuser and seed the data

## [UTILS]
requirements-build:               ## run pip compile and add requirements from the *.in files
	pip-compile -o requirements.txt requirements.in && pip-compile -o requirements-dev.txt requirements-dev.in

requirements-update:              ## run pip compile and rebuild the requirements files
	pip-compile -r -U -o requirements.txt requirements.in && pip-compile -r -U -o requirements-dev.txt requirements-dev.in && chmod a+r requirements.txt && chmod a+r requirements-dev.txt

migrations:                       ## generate migrations in a clean container
	./manage.py makemigrations

migrate:                          ## apply migrations in a clean container
	./manage.py migrate

makemessages:                     ## generate the strings marked for translation
	./manage.py makemessages -a

compilemessages:                  ## compile the translations
	./manage.py compilemessages

collectstatic:
	./manage.py collectstatic --no-input

format:
	black --line-length=120 --target-version=py39  --exclude migrations ./

format-check:
	black --line-length=120 --target-version=py39 --check --diff  --exclude migrations ./
