import tomllib
import uvicorn
from fastapi import FastAPI
from routers import users, items

app = FastAPI()

app.include_router(users.user_router, prefix="/users")
app.include_router(items.item_router, prefix="/items")

# async def root():
#     return {"message": "Hello, FastAPI!"}

if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    server_config = config["server"]

    uvicorn.run(
        app,
        host=server_config["host"],
        port=server_config["port"],
        workers=server_config.get("workers"), # get方法防止key不存在报错
        log_level=server_config.get("log_level"), # get方法防止key不存在报错
        reload=server_config.get("reload") # get方法防止key不存在报错
    )