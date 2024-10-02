from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    discord_id = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)  # Ensure this line exists
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)