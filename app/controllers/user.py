from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
import random
from sqlalchemy import select

faker = Faker()

async def create_user_from_email(
    db: AsyncSession, 
    email=None, 
    username=None, 
    password=None,
    full_name=""
    ):
    from modules.security import hash_password
    user = User(
        username=username,
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password).decode('utf-8'),
        disabled=False
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authorize_user(db: AsyncSession, username: str, password: str) -> User:
    from modules.security import verify_password
    from models import User
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    if user.disabled:
        return None
    return user


async def create_fake_user(db: AsyncSession, user, password):
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