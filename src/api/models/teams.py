from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Teams(Base):
    __tablename__ = 'Teams'
    
    key = Column(BigInteger, primary_key=True, nullable=False, comment='Team unique key')
    name = Column(String(100), nullable=False, comment='Team name')
    status = Column(Integer, default=1, comment='Team status: 1=active, 2=inactive')

    def __repr__(self):
        return f"<Teams(key='{self.key}', name='{self.name}', status='{self.status}')>"
