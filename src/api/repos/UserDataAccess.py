from typing import List
from sqlalchemy.orm import Session
from models.user import User
from repos.DataAccess import DataAccess, db

class UserDataAccess:
    def get_users(self) -> List[User]:
        """
        Retrieve all active users from the database
        
        Returns:
            List[User]: List of active users
        """
        try:
            session = next(db.get_db())
            try:
                return session.query(User).filter(User.status == True).all()
            finally:
                session.close()
        except Exception as e:
            raise Exception(f"Failed to retrieve users: {str(e)}")
    
    def get_user_by_key(self, key: str) -> User:
        """
        Retrieve a user by their unique key
        
        Args:
            key: User's unique key
            
        Returns:
            User: User object if found, None otherwise
        """
        try:
            session = next(db.get_db())
            try:
                return session.query(User).filter(
                    User.key == key,
                    User.status == True
                ).first()
            finally:
                session.close()
        except Exception as e:
            raise Exception(f"Failed to retrieve user with key {key}: {str(e)}")