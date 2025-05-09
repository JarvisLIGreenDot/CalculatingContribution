from typing import List
from sqlalchemy.orm import Session
from models.user import User
from repos.DataAccess import DataAccess, db

class UserDataAccess:
    def get_users(self, teamkey: int = 1, rolekey: int = 1) -> List[User]:
        """
        Retrieve all active users from the database with specified teamkey and rolekey
        
        Args:
            teamkey: Team key to filter by, defaults to 1
            rolekey: Role key to filter by, defaults to 1
        
        Returns:
            List[User]: List of active users with specified teamkey and rolekey
        """
        try:
            session = next(db.get_db())
            try:
                return session.query(User).filter(
                    User.status == 1,
                    User.teamkey == teamkey,
                    User.rolekey == rolekey
                ).all()
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
                    User.status == 1
                ).first()
            finally:
                session.close()
        except Exception as e:
            raise Exception(f"Failed to retrieve user with key {key}: {str(e)}")
    
    def get_user_by_account(self, account: str) -> User:
        """
        Retrieve a user by their account name
        
        Args:
            account: User's account name
            
        Returns:
            User: User object if found, None otherwise
        """
        try:
            session = next(db.get_db())
            try:
                return session.query(User).filter(
                    User.account == account,
                    User.status == 1
                ).first()
            finally:
                session.close()
        except Exception as e:
            raise Exception(f"Failed to retrieve user with account {account}: {str(e)}")