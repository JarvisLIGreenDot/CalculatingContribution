from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    
    key = Column(BigInteger, primary_key=True, nullable=False, comment='User unique key')
    account = Column(String(100), nullable=False, comment='User account name')
    status = Column(Integer, default=1, comment='User status')
    teamkey = Column(BigInteger, default=0, comment='team key')
    rolekey = Column(BigInteger, default=0, comment='role key')

    def __repr__(self):
        return f"<User(key='{self.key}', account='{self.account}')>"