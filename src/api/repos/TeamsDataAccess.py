from typing import List
from models.teams import Teams
from repos.DataAccess import db

class TeamsDataAccess:
    def get_teams(self) -> List[Teams]:
        """
        Retrieve all teams from the database
        
        Returns:
            List[Teams]: List of all teams
        """
        try:
            session = next(db.get_db())
            try:
                return session.query(Teams).all()
            finally:
                session.close()
        except Exception as e:
            raise Exception(f"Failed to retrieve teams: {str(e)}")
