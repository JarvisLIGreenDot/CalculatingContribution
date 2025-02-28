import tomllib
from pathlib import Path
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

class DataAccess:
    def __init__(self):
        try:
            # Get the current file's directory and navigate to config.toml
            current_dir = Path(__file__).resolve().parent.parent
            config_path = current_dir / "config.toml"
            
            if not config_path.exists():
                raise FileNotFoundError(f"config.toml not found at {config_path}")
            
            with open(config_path, "rb") as f:
                config = tomllib.load(f)
            
            db_config = config.get("database", {})
            required_keys = ["user", "password", "host", "port", "database"]
            missing_keys = [key for key in required_keys if key not in db_config]
            
            if missing_keys:
                raise KeyError(f"Missing required database config keys: {missing_keys}")
            
            DATABASE_URL = (
                f"postgresql://{db_config['user']}:{db_config['password']}"
                f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
            )
            
            self.engine = create_engine(DATABASE_URL, echo=False)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.Base = declarative_base()
            
        except Exception as e:
            raise Exception(f"Failed to initialize database connection: {str(e)}")
    
    def get_db(self) -> Session:
        """
        Get database session with automatic cleanup
        
        Yields:
            Session: Database session
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Create global database instance
db = DataAccess()