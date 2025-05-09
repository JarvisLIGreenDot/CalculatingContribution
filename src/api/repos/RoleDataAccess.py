from typing import List
from models.role import Role
from repos.DataAccess import db

class RoleDataAccess:
    def get_roles(self) -> List[Role]:
        """
        Retrieve all roles from the database
        
        Returns:
            List[Role]: List of all roles
        """
        try:
            session = next(db.get_db())
            try:
                return session.query(Role).all()
            finally:
                session.close()
        except Exception as e:
            raise Exception(f"Failed to retrieve roles: {str(e)}")
