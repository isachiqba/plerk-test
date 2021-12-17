#!/usr/bin/env sh

set -x

docker compose down --remove-orphans --volumes
docker compose up --remove-orphans --renew-anon-volumes --no-start
docker compose up postgres --detach

poetry build
docker compose run --rm app mkdir -p /opt/dist
docker compose run --rm --volume=./dist:/src/dist app find /src/dist -name '*.whl' -exec cp {} /opt/dist/ \;
rm -rf dist/*

docker compose run --rm app python -m venv /opt/venv
docker compose run --rm app find /opt/dist/ -name '*.whl' -exec /opt/venv/bin/pip install {} \;

until docker exec plerk-postgres pg_isready --quiet; do
  echo "Waiting for (plerk-postgres) PostgreSQL..."
  sleep 1
done

docker compose run --rm app /opt/venv/bin/django-admin migrate

docker compose run \
  --rm \
  --volume=./docs/assets:/src/docs/assets \
  app \
  /opt/venv/bin/django-admin ingest-transactions --clear --no-input /src/docs/assets/test_database.csv

docker compose up --detach
