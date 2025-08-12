from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from . import crud, models, schemas
from .database import engine, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task Service", version="1.0.0")

@app.on_event("startup")
async def create_tables():
    """Create database tables on startup"""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    logger.info("Database tables created successfully")

async def get_user_id_from_header(x_user_id: Optional[str] = Header(None)) -> int:
    """Extract user ID from header (set by gateway)"""
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
    """Create a new task"""
    try:
        db_task = await crud.create_task(db, task, user_id)
        logger.info(f"Task created successfully: {db_task.id} for user {user_id}")
        return db_task
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/tasks", response_model=List[schemas.TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id_from_header)
):
    """Get all tasks for the current user"""
    try:
        tasks = await crud.get_user_tasks(db, user_id, skip, limit)
        return tasks
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id_from_header)
):
    """Get a specific task"""
    try:
        task = await crud.get_task(db, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Check if task belongs to the user
        if task.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this task"
            )
        
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id_from_header)
):
    """Update a task"""
    try:
        # Check if task exists and belongs to user
        existing_task = await crud.get_task(db, task_id)
        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        if existing_task.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this task"
            )
        
        # Update task
        updated_task = await crud.update_task(db, task_id, task_update)
        logger.info(f"Task updated successfully: {task_id}")
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_user_id_from_header)
):
    """Delete a task"""
    try:
        # Check if task exists and belongs to user
        existing_task = await crud.get_task(db, task_id)
        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        if existing_task.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this task"
            )
        
        # Delete task
        await crud.delete_task(db, task_id)
        logger.info(f"Task deleted successfully: {task_id}")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "task-service"}
