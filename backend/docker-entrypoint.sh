#!/bin/sh
# Applique les migrations Alembic avant de demarrer le serveur applicatif.
# Ainsi le schema de la base de production est toujours a jour avant que
# du trafic ne soit servi (voir DEPLOYMENT.md).
set -e

echo "Applying database migrations (alembic upgrade head)..."
alembic upgrade head

exec "$@"
