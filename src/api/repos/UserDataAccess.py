from typing import List
from sqlalchemy.orm import Session
from models.user import User
from repos.DataAccess import DataAccess, db

class UserDataAccess:
    def __init__(self):
        self.db = db
    
    def get_users(self, session: Session) -> List[User]:
        """
        Retrieve all active users from the database
        
        Args:
            session: Database session
            
        Returns:
            List[User]: List of active users
        """
        try:
            return session.query(User).filter(User.status == True).all()
        except Exception as e:
            raise Exception(f"Failed to retrieve users: {str(e)}")
    
    def get_user_by_key(self, session: Session, key: str) -> User:
        """
        Retrieve a user by their unique key
        
        Args:
            session: Database session
            key: User's unique key
            
        Returns:
            User: User object if found, None otherwise
        """
        try:
            return session.query(User).filter(
                User.key == key,
                User.status == True
            ).first()
        except Exception as e:
            raise Exception(f"Failed to retrieve user with key {key}: {str(e)}")