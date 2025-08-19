from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import OperationalError
from typing import List, Optional
import logging
import asyncio
import asyncpg
from urllib.parse import urlparse

from . import crud, models, schemas
from .database import engine, get_db
from .config import settings  # Assuming you load DATABASE_URL here

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task Service", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    retries = 10
    delay = 3
    db_url = settings.DATABASE_URL

    parsed_url = urlparse(db_url)
    logger.info(f"Connecting to DB at {parsed_url.hostname}:{parsed_url.port}...")

    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Attempting DB connection (attempt {attempt}/{retries})...")
            async with engine.begin() as conn:
                await conn.run_sync(models.Base.metadata.create_all)
            logger.info("✅ Database tables created successfully.")
            break
        except (OperationalError, asyncpg.exceptions.CannotConnectNowError, ConnectionRefusedError) as e:
            logger.warning(f"⚠️ DB not ready: {e}. Retrying in {delay}s...")
            await asyncio.sleep(delay)
        except Exception as e:
            logger.error(f"❌ Unexpected DB error: {e}")
            await asyncio.sleep(delay)
    else:
        logger.critical("🔥 Could not connect to the database after retries. Exiting.")
        raise RuntimeError("Database connection failed")


async def get_user_id_from_header(x_user_id: Optional[str] = Header(None)) -> int:
    if not x_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not provided"
        )
    try:
        return int(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID"
        )


@app.post("/tasks", response_model=schemas.TaskResponse)
async def create_task(
    task: schemas.TaskCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id_from_header)
):
    try:
        db_task = await crud.create_task(db, task, user_id)
        logger.info(f"Task created: {db_task.id} for user {user_id}")
        return db_task
    except Exception as e:
        logger.error(f"Create task error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/tasks", response_model=List[schemas.TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id_from_header)
):
    try:
        tasks = await crud.get_user_tasks(db, user_id, skip, limit)
        return tasks
    except Exception as e:
        logger.error(f"Get tasks error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id_from_header)
):
    try:
        task = await crud.get_task(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this task")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get task error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id_from_header)
):
    try:
        task = await crud.get_task(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        updated = await crud.update_task(db, task_id, task_update)
        logger.info(f"Task updated: {task_id}")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update task error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id_from_header)
):
    try:
        task = await crud.get_task(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this task")

        await crud.delete_task(db, task_id)
        logger.info(f"Task deleted: {task_id}")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete task error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        db_status = "up"
    except Exception as e:
        logger.warning(f"DB health check failed: {e}")
        db_status = "down"

    return {
        "status": "healthy",
        "database": db_status,
        "service": "task-service"
    }