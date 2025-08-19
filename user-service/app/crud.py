from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from . import models, schemas

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

async def get_user_by_email(db: AsyncSession, email: str) -> models.User:
    """Get user by email"""
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> models.User:
    """Get user by username"""
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int) -> models.User:
    """Get user by ID"""
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def authenticate_user(db: AsyncSession, username: str, password: str) -> models.User:
    """Authenticate user with username and password"""
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

    