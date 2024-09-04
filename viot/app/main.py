import uvicorn

from app.bootstrap import create_app
from app.common.logging import setup_logging
from app.config import app_settings

setup_logging()


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=app_settings.API_PORT,
        server_header=False,
        date_header=False,
        log_config=None,
        reload=app_settings.ENV == "dev",
        workers=app_settings.WORKERS,
        proxy_headers=True,
    )
