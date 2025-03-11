#!/command/with-contenv sh
# shellcheck shell=bash

# Convert one parameter to uppercase
to_uppercase() {
    echo "${1}" | tr '[:lower:]' '[:upper:]'
}

# Check if the parameter is string True/False and return it as success/failure
is_enabled() {
    _UPPER_VALUE=$(to_uppercase "${1}")
    if [ "${_UPPER_VALUE}" = "TRUE" ]; then
        return 0
  fi

    return 1
}

cd "${BACKEND_ROOT:-/var/www/sdu/backend}" || exit 1

echo "Waiting for the database to be ready"
python3 manage.py wait_for_db

echo "Running Django self-checks"
python3 manage.py check

# Run the database migrations
if is_enabled "${RUN_MIGRATIONS}"; then
    echo "Migrating database"
    python3 manage.py migrate --run-syncdb
    python3 manage.py createcachetable
fi

# Compile the translation messages
if is_enabled "${RUN_COMPILE_MESSAGES}"; then
    echo "Compiling translation messages"
    python3 manage.py compilemessages
fi

# Collect the static files
if is_enabled "${RUN_COLLECT_STATIC}"; then
    echo "Collecting static files"
    mkdir -p static
    python3 manage.py collectstatic --noinput
fi

if is_enabled "${RUN_SEED_GROUPS}"; then
  ./manage.py seed_groups
fi

if is_enabled "${RUN_CREATE_SUPER_USER}"; then
  ./manage.py seed_superuser
fi

if is_enabled "${RUN_SEED_SCHEDULE}"; then
  ./manage.py seed_schedule
fi

if is_enabled "${RUN_SEED_DATA}"; then
  echo "Load seed data in the database"
  ./manage.py seed_item_data
  ./manage.py seed_transport_service_categories
  ./manage.py seed_volunteering_types
fi
