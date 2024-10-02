import asyncio
from database import SessionLocal, engine
from db.factories import seed_users  # Import factory from /app/db
from models import Base

async def seed():
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Open async session and run the seeder
    async with SessionLocal() as session:
        await seed_users(session, num_users=10)

if __name__ == "__main__":
    asyncio.run(seed())