from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ApplicationConfiguration(Base):
    __tablename__ = 'applicationconfiguration'
    
    key = Column(BigInteger, primary_key=True, nullable=False, comment='Configuration key')
    name = Column(String(100), nullable=False, comment='Configuration name')
    value = Column(String(500), nullable=True, comment='Configuration value')
    status = Column(Integer, default=1, comment='Status flag')
    isdeleted = Column(Integer, default=0, comment='Deletion flag')

    def __repr__(self):
        return f"<ApplicationConfiguration(key='{self.key}', name='{self.name}')>"