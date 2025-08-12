from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from . import crud, models, schemas, auth
from .database import engine, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="User Service", version="1.0.0")

@app.on_event("startup")
async def create_tables():
    """Create database tables on startup"""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    logger.info("Database tables created successfully")

@app.post("/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = await crud.get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        existing_username = await crud.get_user_by_username(db, user.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        db_user = await crud.create_user(db, user)
        logger.info(f"User registered successfully: {user.username}")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.post("/login", response_model=schemas.Token)
async def login(user_credentials: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT token"""
    try:
        # Authenticate user
        user = await crud.authenticate_user(db, user_credentials.username, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = auth.create_access_token(data={"sub": user.username, "user_id": user.id})
        logger.info(f"User logged in successfully: {user.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/users/me", response_model=schemas.UserResponse)
async def get_current_user_info(current_user: models.User = Depends(auth.get_current_user)):
    """Get current user information"""
    return current_user

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "user-service"}