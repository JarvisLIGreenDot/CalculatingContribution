import tomllib
import uvicorn
from fastapi import FastAPI
from api.routers import users_controller, contributions_controller
from config.load_config import app_settings

app = FastAPI()

app.include_router(contributions_controller.router)

if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    server_config = config["server"]

    uvicorn.run(
        app,
        host=app_settings.server.host,
        port=app_settings.server.port,
        workers=app_settings.server.workers,
        log_level=app_settings.server.log_level,
        reload=app_settings.server.reload
    )


