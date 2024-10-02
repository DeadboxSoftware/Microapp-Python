from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
import random

# Faker instance to generate fake data
faker = Faker()

async def create_fake_user(db: AsyncSession):
    """Create a single fake user."""
    fake_user = User(
        username=faker.user_name(),
        full_name=faker.name(),
        email=faker.email(),
        hashed_password=faker.password(),
        disabled=random.choice([True, False])
    )
    db.add(fake_user)
    await db.commit()
    await db.refresh(fake_user)
    return fake_user

async def seed_users(db: AsyncSession, num_users: int = 10):
    """Generate and seed multiple fake users."""
    for _ in range(num_users):
        await create_fake_user(db)
    print(f"Seeded {num_users} fake users.")