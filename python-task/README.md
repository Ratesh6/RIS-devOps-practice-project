# Project: Dockerized FastAPI Microservices with Localhost Deployment

This project already includes three working Python/FastAPI microservices:

- **User Service** – Handles authentication, registration, and JWT-based login.  
- **Task Service** – Manages CRUD operations for to-do items with user ownership.  
- **Gateway Service** – Acts as an API gateway, routing requests between services.  

Your job is to **containerize, orchestrate, and serve these services locally**.  
The application code is ready — you are focusing on **deployment setup**.

---

## 📌 Your Tasks

### **1. Dockerization**
Write a **Dockerfile** for each service (`user-service`, `task-service`, `gateway-service`) using **Python 3.11+**.

Each container should:
- Install dependencies from `requirements.txt`
- Run the FastAPI app with **Uvicorn**
- Expose the correct port
- Use environment variables for configuration

---

### **2. Docker Compose Setup**
Create a `docker-compose.yml` to run:
- The three FastAPI services
- **Two PostgreSQL containers** (one for user-service, one for task-service)
- **Nginx** as a reverse proxy to the gateway service

Requirements:
- Configure **networks** so services communicate via Docker service names
- Add any `docker-compose.dev.yml` overrides you think are useful

---

### **3. Database Initialization**
- Mount the provided SQL files from `database/init-scripts/` so PostgreSQL containers **auto-create databases and schemas**.
- Ensure environment variables (`DB name`, `user`, `password`, `host`) are set in Compose.

---

### **4. Nginx Reverse Proxy**
Configure **Nginx** to:
- Forward incoming requests to the **gateway service**
- Enable **CORS headers** for API access
- Be ready for **multiple gateway instances** (basic load balancing)

**Phase 1**: use **localhost** as the only domain — no custom DNS needed yet.

---

### **5. Service Communication**
- Services communicate over HTTP/JSON via the **gateway**.
- Ensure each service URL points to its Docker network name (e.g., `user-service:8000`).
- Add retry logic and health checks if needed.

---

## 🔐 Important Notes
- All variables in `.env` files are just examples. Replace them with your own values where needed (**DB credentials, JWT secret keys, ports, etc.**).
- **Phase 1**: Everything runs locally on **localhost** — no public domain or HTTPS setup.
- Custom domains and TLS can be explored in **Phase 2**.

---

## 🛠 Onboarding Checklist (Beginner-Friendly)

### **Step 1: Set up your environment**
1. Install Docker and Docker Compose  
2. Clone the repository  
3. Review the `.env` files (replace sample values as needed)

---

### **Step 2: Write Dockerfiles**
One for each service: `user-service`, `task-service`, `gateway-service`.

**Base image**: `python:3.11-slim`  
Steps:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

## **Step 3: Set up Docker Compose**
Create a **`docker-compose.yml`** file with:

- `user-service` container  
- `task-service` container  
- `gateway-service` container  
- **Two PostgreSQL containers** with mounted init scripts  
- `nginx` container  

**Requirement:** Ensure all services are in the **same network**.

---

## **Step 4: Configure Nginx**
Create **`nginx.conf`** to:
- Reverse proxy **all incoming requests** to `gateway-service`
- Enable **CORS headers**
- Keep domain as **localhost** for now

---

## **Step 5: Test locally**
```bash
docker compose up --build
```

## **Step 6: Clean up**

To stop and remove all running containers:
```bash
docker compose down
