# Viot Backend
This is the backend for the Viot project. It is a FastAPI application that uses Celery for background tasks and Redis for task distribution.

## Requirements
- Docker & Docker Compose
- Poetry

## Local development
1. Start the docker containers with Docker Compose:
   ```
   docker compose up -d
   ```

2. Run the following command to migrate the database:
   ```
    chmod +x ./scripts/migrate.sh
    ./scripts/migrate.sh
    ```

3. The application should now be running and accessible at:
- API: `http://api.viot.local/docs` (Swagger UI)
- Celery Flower: `http://flower/` (Account login: `admin/admin`)
- Mailpit: `http://mailpit/` (Account login: `admin/admin`)


### Local development with Poetry

1. Install the dependencies:
   ```
   poetry install
   ```

2. Activate the virtual environment:
   ```
   poetry shell
   ```

3. Migrate the database:
   ```
   alembic upgrade head
   ```

4. Start the FastAPI application:
   ```
   python app/main.py
   ```

5. Access Swagger UI at: `http://localhost:8000/docs`


## Testing
We use Pytest for running our test suite and [Testcontainers](https://testcontainers.com/) for managing isolated testing dependencies.

1. Run with docker

   Start the docker containers with Docker Compose:
   ```
   docker compose up -d
   ```

   Run the following command to run the test suite with docker:
   ```
   docker compose exec -it viot-api pytest
   ```

   With coverage:
   ```
   docker compose exec -it viot-api coverage run -m pytest -v
   docker compose exec -it viot-api coverage report
   ```

2. Without docker

   Run the following command to run the test suite:
   ```
   pytest
   ```

   With coverage:
   ```
   coverage run -m pytest
   coverage report
   ```

   For faster test execution we use `pytest-xdist`, use the following command:
   ```
   coverage run -m pytest -n auto
   ```
   Warning: `pytest-xdist` does not work correctly with `coverage` when running the tests with coverage so the coverage report will not be accurate.
