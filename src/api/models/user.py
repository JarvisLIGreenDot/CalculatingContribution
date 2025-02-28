from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(50), nullable=False, unique=True, comment='User unique key')
    account = Column(String(100), nullable=False, comment='User account name')
    status = Column(Boolean, default=True, comment='User status')

    def __repr__(self):
        return f"<User(key='{self.key}', account='{self.account}')>"