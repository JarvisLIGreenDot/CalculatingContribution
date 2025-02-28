from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ApplicationConfiguration(Base):
    __tablename__ = 'applicationconfiguration'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(50), nullable=False, unique=True, comment='Configuration key')
    name = Column(String(100), nullable=False, comment='Configuration name')
    value = Column(String(500), nullable=True, comment='Configuration value')
    status = Column(Boolean, default=True, comment='Status flag')
    isdeleted = Column(Boolean, default=False, comment='Deletion flag')

    def __repr__(self):
        return f"<ApplicationConfiguration(key='{self.key}', name='{self.name}')>"