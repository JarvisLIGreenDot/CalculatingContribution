import tomllib
from pathlib import Path
from typing import Optional

from models.app_settings import AppSettings

def load_config(config_path: Optional[Path] = None) -> AppSettings:
    """
    Load configuration from config.toml file
    Args:
        config_path: Optional path to config file. If None, uses default locations
    Returns:
        AppSettings instance with loaded configuration
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.toml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")
        
    with open(config_path, "rb") as f:
        config_data = tomllib.load(f)
        
    return AppSettings.from_toml(config_data)

def get_app_settings() -> AppSettings:
    """Get application settings from default config location"""
    return load_config()

# 获取配置的具体实例
settings = get_app_settings()

# 导出配置,供其他模块使用
app_settings = settings