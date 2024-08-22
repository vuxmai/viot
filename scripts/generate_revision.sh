# Check parameter
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <message>"
  exit 1
fi

MESSAGE=$1
SERVICE_NAME="viot-api"

# Check if Docker Compose service is running
if ! docker compose ps | grep -q $SERVICE_NAME; then
  echo "Docker Compose service `$SERVICE_NAME` is not running. Please start the service first."
  exit 1
fi

# Generate Alembic revision with current user permissions
docker compose exec -T --user $(id -u):$(id -g) $SERVICE_NAME alembic revision --autogenerate -m "$MESSAGE"

# Check if Alembic revision generated successfully
if [ $? -eq 0 ]; then
  echo "Alembic revision generated successfully."
else
  echo "Failed to generate Alembic revision."
  exit 1
fi
