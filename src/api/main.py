import tomllib
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from routers import contributions_controller
from config.load_config import app_settings

app = FastAPI()

app.include_router(contributions_controller.router)

if __name__ == "__main__":
    # Get the current file's directory and config.toml path
    current_dir = Path(__file__).resolve().parent
    config_path = current_dir / "config.toml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"config.toml not found at {config_path}")
    
    with open(config_path, "rb") as f:
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


