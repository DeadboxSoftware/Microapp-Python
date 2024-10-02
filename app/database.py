from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DB_STRING")
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
# Base class for models
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session



async def get_or_create_user(db: AsyncSession, discord_id: str, username: str, email: str, avatar_url: str, token: dict):
    from models import User
    result = await db.execute(select(User).where(User.discord_id == discord_id))
    user = result.scalars().first()
    if not user:
        user = User(
            discord_id=discord_id,
            username=username,
            email=email,
            avatar_url=avatar_url,
            access_token=token.get('access_token'),
            refresh_token=token.get('refresh_token')
        )
        db.add(user)
        await db.commit()  # Commit changes
        await db.refresh(user)  # Refresh to get the latest data from the database

    return user