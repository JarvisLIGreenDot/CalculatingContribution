from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class ServerSettings:
    host: str
    port: int
    workers: int
    log_level: str
    reload: bool

@dataclass
class ApiSettings:
    title: str
    description: str
    version: str
    docs_url: str
    redoc_url: Optional[str] = None

@dataclass
class AppSettings:
    server: ServerSettings
    api: ApiSettings
    
    @classmethod
    def from_toml(cls, config_data: dict) -> 'AppSettings':
        server_settings = ServerSettings(
            host=config_data["server"]["host"],
            port=config_data["server"]["port"],
            workers=config_data["server"]["workers"],
            log_level=config_data["server"]["log_level"],
            reload=config_data["server"]["reload"]
        )
        
        # 使用默认值，如果配置中没有相应的设置
        api_config = config_data.get("api", {})
        api_settings = ApiSettings(
            title=api_config.get("title", "GitHub Contributions API"),
            description=api_config.get("description", "API for tracking GitHub contributions"),
            version=api_config.get("version", "0.1.0"),
            docs_url=api_config.get("docs_url", "/docs"),
            redoc_url=api_config.get("redoc_url", "/redoc")
        )
        
        return cls(server=server_settings, api=api_settings)