from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
import httpx
import os
import logging
from typing import Optional
from jose import JWTError, jwt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gateway Service", version="1.0.0")

# Service URLs from environment
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8000")
TASK_SERVICE_URL = os.getenv("TASK_SERVICE_URL", "http://localhost:8001")

# JWT settings (same as user service)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

class JWTValidator:
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            logger.error(f"JWT verification failed: {str(e)}")
            return None

async def get_current_user_from_token(request: Request) -> Optional[dict]:
    """Extract and verify user from Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.split(" ")[1]
    return JWTValidator.verify_token(token)

@app.post("/register")
async def register(request: Request):
    """Forward registration request to User Service"""
    try:
        body = await request.body()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{USER_SERVICE_URL}/register",
                content=body,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except httpx.RequestError as e:
        logger.error(f"Error forwarding registration request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.post("/login")
async def login(request: Request):
    """Forward login request to User Service"""
    try:
        body = await request.body()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{USER_SERVICE_URL}/login",
                content=body,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except httpx.RequestError as e:
        logger.error(f"Error forwarding login request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/users/me")
async def get_current_user(request: Request):
    """Forward get current user request to User Service"""
    try:
        # Verify authentication
        user_data = await get_current_user_from_token(request)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token"
            )
        
        auth_header = request.headers.get("Authorization")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{USER_SERVICE_URL}/users/me",
                headers={"Authorization": auth_header},
                timeout=30.0
            )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except HTTPException:
        raise
    except httpx.RequestError as e:
        logger.error(f"Error forwarding get user request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error getting user info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/tasks")
async def get_tasks(request: Request):
    """Forward get tasks request to Task Service with authentication"""
    try:
        # Verify authentication
        user_data = await get_current_user_from_token(request)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token"
            )
        
        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        
        # Forward request to task service
        headers = {"X-User-Id": str(user_id)}
        
        # Add query parameters if present
        url = f"{TASK_SERVICE_URL}/tasks"
        if request.url.query:
            url += f"?{request.url.query}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=url,
                headers=headers,
                timeout=30.0
            )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except HTTPException:
        raise
    except httpx.RequestError as e:
        logger.error(f"Error forwarding get tasks request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Task service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error getting tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.post("/tasks")
async def create_task(request: Request):
    """Forward create task request to Task Service with authentication"""
    try:
        # Verify authentication
        user_data = await get_current_user_from_token(request)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token"
            )
        
        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        
        # Forward request to task service
        body = await request.body()
        headers = {"Content-Type": "application/json", "X-User-Id": str(user_id)}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TASK_SERVICE_URL}/tasks",
                content=body,
                headers=headers,
                timeout=30.0
            )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except HTTPException:
        raise
    except httpx.RequestError as e:
        logger.error(f"Error forwarding create task request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Task service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.put("/tasks/{task_id}")
async def update_task(request: Request, task_id: int):
    """Forward update task request to Task Service with authentication"""
    try:
        # Verify authentication
        user_data = await get_current_user_from_token(request)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token"
            )
        
        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        
        # Forward request to task service
        body = await request.body()
        headers = {"Content-Type": "application/json", "X-User-Id": str(user_id)}
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{TASK_SERVICE_URL}/tasks/{task_id}",
                content=body,
                headers=headers,
                timeout=30.0
            )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except HTTPException:
        raise
    except httpx.RequestError as e:
        logger.error(f"Error forwarding update task request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Task service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error updating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.delete("/tasks/{task_id}")
async def delete_task(request: Request, task_id: int):
    """Forward delete task request to Task Service with authentication"""
    try:
        # Verify authentication
        user_data = await get_current_user_from_token(request)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token"
            )
        
        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        
        # Forward request to task service
        headers = {"X-User-Id": str(user_id)}
        
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{TASK_SERVICE_URL}/tasks/{task_id}",
                headers=headers,
                timeout=30.0
            )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except HTTPException:
        raise
    except httpx.RequestError as e:
        logger.error(f"Error forwarding delete task request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Task service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/tasks/{task_id}")
async def get_task(request: Request, task_id: int):
    """Forward get single task request to Task Service with authentication"""
    try:
        # Verify authentication
        user_data = await get_current_user_from_token(request)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token"
            )
        
        user_id = user_data.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        
        # Forward request to task service
        headers = {"X-User-Id": str(user_id)}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{TASK_SERVICE_URL}/tasks/{task_id}",
                headers=headers,
                timeout=30.0
            )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except HTTPException:
        raise
    except httpx.RequestError as e:
        logger.error(f"Error forwarding get task request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Task service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error getting task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/health")
async def health_check():
    """Gateway health check endpoint"""
    try:
        # Check if dependent services are healthy
        async with httpx.AsyncClient() as client:
            # Check user service
            try:
                user_health = await client.get(f"{USER_SERVICE_URL}/health", timeout=5.0)
                user_status = user_health.status_code == 200
            except:
                user_status = False
            
            # Check task service
            try:
                task_health = await client.get(f"{TASK_SERVICE_URL}/health", timeout=5.0)
                task_status = task_health.status_code == 200
            except:
                task_status = False
        
        return {
            "status": "healthy" if user_status and task_status else "degraded",
            "service": "gateway-service",
            "dependencies": {
                "user-service": "healthy" if user_status else "unhealthy",
                "task-service": "healthy" if task_status else "unhealthy"
            }
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "gateway-service",
            "error": str(e)
        }

        