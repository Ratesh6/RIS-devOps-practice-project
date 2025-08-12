from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 200:
            raise ValueError('Title must be less than 200 characters')
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    
    @validator('title')
    def validate_title(cls, v):
        if v is not None:
            if len(v.strip()) == 0:
                raise ValueError('Title cannot be empty')
            if len(v) > 200:
                raise ValueError('Title must be less than 200 characters')
            return v.strip()
        return v

class TaskResponse(TaskBase):
    id: int
    completed: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True