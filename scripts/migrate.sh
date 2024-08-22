SERVICE_NAME="viot-api"

# Migrate
docker compose exec -T $SERVICE_NAME alembic upgrade head
