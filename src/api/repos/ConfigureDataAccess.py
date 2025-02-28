from typing import List
from sqlalchemy.orm import Session
from models.application_configuration import ApplicationConfiguration
from repos.DataAccess import DataAccess, db

class ConfigureDataAccess:
    def __init__(self):
        self.db = db
    
    def get_configurations(self, session: Session) -> List[ApplicationConfiguration]:
        """
        Retrieve all active configurations from the database
        
        Args:
            session: Database session
            
        Returns:
            List[ApplicationConfiguration]: List of active configurations
        """
        try:
            return session.query(ApplicationConfiguration).filter(
                ApplicationConfiguration.status == True,
                ApplicationConfiguration.isdeleted == False
            ).all()
        except Exception as e:
            raise Exception(f"Failed to retrieve configurations: {str(e)}")
    
    def get_configuration_by_key(self, session: Session, key: str) -> ApplicationConfiguration:
        """
        Retrieve a configuration by its key
        
        Args:
            session: Database session
            key: Configuration key
            
        Returns:
            ApplicationConfiguration: Configuration object if found, None otherwise
        """
        try:
            return session.query(ApplicationConfiguration).filter(
                ApplicationConfiguration.key == key,
                ApplicationConfiguration.status == True,
                ApplicationConfiguration.isdeleted == False
            ).first()
        except Exception as e:
            raise Exception(f"Failed to retrieve configuration with key {key}: {str(e)}")