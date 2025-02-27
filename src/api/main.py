import tomllib
import uvicorn
from fastapi import FastAPI
from routers import users
from config.load_config import app_settings

app = FastAPI()

app.include_router(users.user_router, prefix="/users")
# app.include_router(items.item_router, prefix="/items")


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    server_config = config["server"]

    uvicorn.run(
        app,
        host=app_settings.server.host,
        port=app_settings.server.port,
        workers=app_settings.server.workers, # get方法防止key不存在报错
        log_level=app_settings.server.log_level, # get方法防止key不存在报错
        reload=app_settings.server.reload # get方法防止key不存在报错
    )