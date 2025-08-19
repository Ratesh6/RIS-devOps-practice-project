from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
from . import models, schemas

async def create_task(db: AsyncSession, task: schemas.TaskCreate, owner_id: int) -> models.Task:
    """Create a new task"""
    db_task = models.Task(
        title=task.title,
        description=task.description,
        owner_id=owner_id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def get_task(db: AsyncSession, task_id: int) -> Optional[models.Task]:
    """Get a task by ID"""
    result = await db.execute(select(models.Task).where(models.Task.id == task_id))
    return result.scalar_one_or_none()

async def get_user_tasks(db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.Task]:
    """Get all tasks for a specific user"""
    result = await db.execute(
        select(models.Task)
        .where(models.Task.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .order_by(models.Task.created_at.desc())
    )
    return result.scalars().all()

async def update_task(db: AsyncSession, task_id: int, task_update: schemas.TaskUpdate) -> models.Task:
    """Update a task"""
    # Get the current task
    task = await get_task(db, task_id)
    if not task:
        return None
    
    # Update fields that are provided
    update_data = task_update.dict(exclude_unset=True)
    if update_data:
        await db.execute(
            update(models.Task)
            .where(models.Task.id == task_id)
            .values(**update_data)
        )
        await db.commit()
        await db.refresh(task)
    
    return task

async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """Delete a task"""
    result = await db.execute(delete(models.Task).where(models.Task.id == task_id))
    await db.commit()
    return result.rowcount > 0