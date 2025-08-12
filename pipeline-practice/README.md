# Intern Project Task – CI/CD Pipeline with Docker & GitHub Actions

Welcome! This project is designed to help you understand the fundamentals of **CI/CD**, **Docker**, and **GitHub Actions** by working through a real-world development workflow.

---

## 📌 Project Objective

You will set up and automate the containerization and deployment of a Python web application with a PostgreSQL database using:

- Docker
- Docker Compose
- GitHub Actions
- Docker Hub

---

## ✅ Task Instructions

### 1. 🔗 Fork This Repository

Start by forking this repository to your own GitHub account. Clone the forked repository to your local machine:

```bash
git clone https://github.com/Retouch-It-Services/RIS-devOps-practice-project.git
```

---

### 2. 🗄️ Setup PostgreSQL Database Locally

You will need a PostgreSQL database running locally.

- Either install PostgreSQL manually **or** run it using **Docker Compose** (preferred).
- Create a `.env` file in the root directory of your project with the following environment variables:

```env
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
```

---

### 3. 🐳 Write a Dockerfile for Your Python Application

You will create a `Dockerfile` to containerize your Python application.

Your `Dockerfile` should include the following steps:

- ✅ **Use a Python base image**  
  For example: `python:3.11-slim`

- ✅ **Set the working directory**  
  This defines where commands will be run inside the container.

- ✅ **Copy the application code**  
  Include the relevant project files inside the image.

- ✅ **Install dependencies**  
  Run `pip install -r requirements.txt` to install all necessary Python packages.

- ✅ **Define a default command**  
  Use `CMD` or `ENTRYPOINT` to specify how to start the application (e.g., `CMD ["python", "app.py"]`).

> ⚠️ Be sure your `requirements.txt` is up to date and includes all necessary packages.

📘 **Reference**: [Dockerfile Documentation](https://docs.docker.com/engine/reference/builder/)

---

### 4. 🧩 Create a `docker-compose.yml`

You will define your multi-container setup using Docker Compose.

Your `docker-compose.yml` file should include **two services**:

- **`app`** – Your Python application, built from your custom `Dockerfile`
- **`db`** – A PostgreSQL database service using the official `postgres` image

#### ✅ Your Compose file should include:

- **Volumes**  
  Use Docker volumes to persist PostgreSQL data, even after containers are stopped or removed.

- **Networks**  
  Ensure both containers are on the same network so they can communicate. Your app should connect to the database using `DB_HOST=db`.

- **Environment Variables**  
  Set the database service environment using variables from your `.env` file (e.g., `POSTGRES_DB`, `POSTGRES_USER`, etc.).

📘 **Reference**: [Docker Compose File Reference](https://docs.docker.com/compose/compose-file/)

---

### 5. 🧪 Test It Locally

Once your `Dockerfile` and `docker-compose.yml` are ready, you should test everything **locally** to ensure the setup works as expected.

#### ✅ Run the following command from your project root:

```bash
docker-compose up --build
```

---

### 6. ☁️ Push to GitHub and Set Up GitHub Actions

Once you've confirmed that your application works correctly using Docker Compose locally, it's time to automate the build and deployment process using **GitHub Actions**.

#### ✅ Steps:

1. **Push your code** to your GitHub repository (including your `Dockerfile`, `docker-compose.yml`, and `.github/workflows/` directory).

2. Inside `.github/workflows/`, create a workflow file named `ci-cd.yml` (or similar).

3. Your workflow should include the following steps:

   - **Trigger**: Run the workflow on every `push` to the `main` branch.
   - **Build**: Build your Python application Docker image using your `Dockerfile`.
   - **Authenticate**: Log in to Docker Hub using GitHub Secrets.
   - **Push**: Push the built image to your Docker Hub repository.

> 🧠 **Note**: You only need to build and push your **application image**.  
> The **PostgreSQL image** is pulled from Docker Hub as an official image and does not need to be built or pushed by you.

📘 **References**:

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Publishing Docker Images with GitHub Actions](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)

---

### 🔐 GitHub Secrets Required

To securely log in to Docker Hub during the workflow, you must store your credentials as GitHub **repository secrets**.

#### ✅ Steps:

1. Go to your GitHub repository.
2. Navigate to **Settings → Secrets and variables → Actions**.
3. Click **"New repository secret"**.
4. Add the following secrets:

| Name              | Description                         |
|-------------------|-------------------------------------|
| `DOCKER_USERNAME` | Your Docker Hub username            |
| `DOCKER_PASSWORD` | Your Docker Hub password or token   |

> 🔒 Secrets are encrypted and not visible in the code or logs.

---

## 🚀 Getting Started

1. Fork this repository
2. Clone your fork locally
3. Set up your local PostgreSQL database or use Docker Compose
4. Create your `.env` file with database credentials
5. Write your `Dockerfile` and `docker-compose.yml`
6. Test locally with `docker-compose up --build`
7. Set up GitHub Actions workflow
8. Configure Docker Hub secrets in GitHub
9. Push your code and watch the CI/CD pipeline in action!

---

## 🎯 Learning Outcomes

By completing this project, you will gain hands-on experience with:

- Creating Docker containers for Python applications
- Setting up multi-container applications with Docker Compose
- Implementing CI/CD pipelines with GitHub Actions
- Managing secrets and environment variables securely
- Publishing Docker images to Docker Hub
- Database integration with PostgreSQL

---

## 🤝 Support

If you encounter any issues or have questions, please:

1. Check the documentation links provided
2. Review your configuration files for syntax errors
3. Ensure all secrets are properly configured in GitHub
4. Test your setup locally before pushing to GitHub

Happy learning! 🎉
