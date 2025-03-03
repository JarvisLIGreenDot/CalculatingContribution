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
class AppSettings:
    server: ServerSettings
    
    @classmethod
    def from_toml(cls, config_data: dict) -> 'AppSettings':
        server_settings = ServerSettings(
            host=config_data["server"]["host"],
            port=config_data["server"]["port"],
            workers=config_data["server"]["workers"],
            log_level=config_data["server"]["log_level"],
            reload=config_data["server"]["reload"]
        )
        
        return cls(server=server_settings)