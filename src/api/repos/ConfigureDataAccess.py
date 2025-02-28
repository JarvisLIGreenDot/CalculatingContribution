from typing import List
from models.application_configuration import ApplicationConfiguration
from repos.DataAccess import db

class ConfigureDataAccess:
    def get_configurations(self) -> List[ApplicationConfiguration]:
        """
        Retrieve all active configurations from the database
        
        Returns:
            List[ApplicationConfiguration]: List of active configurations
        """
        try:
            session = next(db.get_db())
            try:
                return session.query(ApplicationConfiguration).filter(
                    ApplicationConfiguration.status == True,
                    ApplicationConfiguration.isdeleted == False
                ).all()
            finally:
                session.close()
        except Exception as e:
            raise Exception(f"Failed to retrieve configurations: {str(e)}")
    
    def get_configuration_by_key(self, key: str) -> ApplicationConfiguration:
        """
        Retrieve a configuration by its key
        
        Args:
            key: Configuration key
            
        Returns:
            ApplicationConfiguration: Configuration object if found, None otherwise
        """
        try:
            session = next(db.get_db())
            try:
                return session.query(ApplicationConfiguration).filter(
                    ApplicationConfiguration.key == key,
                    ApplicationConfiguration.status == True,
                    ApplicationConfiguration.isdeleted == False
                ).first()
            finally:
                session.close()
        except Exception as e:
            raise Exception(f"Failed to retrieve configuration with key {key}: {str(e)}")