from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.dialects.postgresql as pg
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, nullable=False)
    name = Column(String(55), nullable=False)
    username = Column(String(30), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default='user')
    picture_url = Column(String(600), nullable=True)
    logins = Column(Integer, default=0)
    last_ip = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_activity_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, name={self.name})>"
