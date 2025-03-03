import logging
from pathlib import Path

# 创建日志目录
log_path = Path(__file__).parent.parent / "logs"
log_path.mkdir(exist_ok=True)

# 日志格式
log_format = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def setup_logging():
    # 获取根日志记录器
    logger = logging.getLogger("api")
    logger.setLevel(logging.INFO)

    # 文件处理器
    file_handler = logging.FileHandler(
        log_path / "api.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(log_format)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 创建日志实例
logger = setup_logging()