from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = 'role'
    
    key = Column(BigInteger, primary_key=True, nullable=False, comment='Role unique key')
    rolename = Column(String(100), nullable=False, comment='Role name')
    status = Column(Integer, default=1, comment='Role status: 1=active, 2=inactive')

    def __repr__(self):
        return f"<Role(key='{self.key}', name='{self.name}', status='{self.status}')>"
