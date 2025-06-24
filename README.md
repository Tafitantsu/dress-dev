# Microservices Project with Docker

## Project Overview

This project demonstrates a microservices architecture using Docker and Docker Compose. It includes several backend services built with FastAPI (Python), a frontend application built with React (Vite), and PostgreSQL databases for data persistence. An Nginx gateway service acts as a reverse proxy, routing requests to the appropriate microservice.

## Microservices & Responsibilities

The application is composed of the following services:

*   **Frontend (`frontend`)**:
    *   Responsibilities: Provides the user interface for the application.
    *   Technology: React (Vite), JavaScript, HTML, CSS.
    *   Served by: Nginx (within its own Docker container).
*   **Gateway Service (`gateway-service`)**:
    *   Responsibilities: Acts as a reverse proxy and single entry point for all client requests. Routes requests to the appropriate backend service or the frontend.
    *   Technology: Nginx.
*   **Authentication Service (`auth-service`)**:
    *   Responsibilities: Manages user registration, login, and token-based authentication (JWT).
    *   Technology: FastAPI (Python), PostgreSQL.
    *   Database: `auth-db` (PostgreSQL instance).
*   **Content Service (`content-service`)**:
    *   Responsibilities: Manages content items (e.g., articles, posts). Provides CRUD operations for content.
    *   Technology: FastAPI (Python), PostgreSQL.
    *   Database: `content-db` (PostgreSQL instance).
*   **Suggestion Service (`suggestion-service`)**:
    *   Responsibilities: Provides content suggestions or recommendations. (Currently uses simulated data).
    *   Technology: FastAPI (Python).
*   **Database Services (`auth-db`, `content-db`)**:
    *   Responsibilities: Provide persistent storage for the `auth-service` and `content-service` respectively.
    *   Technology: PostgreSQL.

## Tech Stack

*   **Backend Framework**: FastAPI (Python)
*   **Frontend Framework**: React (Vite)
*   **Databases**: PostgreSQL
*   **Containerization**: Docker, Docker Compose
*   **Reverse Proxy**: Nginx

## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
*   **Docker Compose**: Usually included with Docker Desktop. If not, [install Docker Compose](https://docs.docker.com/compose/install/).

## Setup Instructions

Follow these steps to get the application running locally using Docker Compose:

1.  **Clone the Repository (if you haven't already):**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Create Environment Files:**
    Each backend service requires a `.env` file for its configuration. Example files (`.env.example`) are provided in each service directory.

    *   **Auth Service (`services/auth-service/.env`):**
        Copy `services/auth-service/.env.example` to `services/auth-service/.env`.
        The `DATABASE_URL` should be:
        `DATABASE_URL="postgresql://auth_user:auth_password@auth-db:5432/auth_db"`
        Ensure you set a strong `SECRET_KEY` for JWT generation.
        ```env
        # services/auth-service/.env
        DATABASE_URL="postgresql://auth_user:auth_password@auth-db:5432/auth_db"
        SECRET_KEY="your-super-strong-secret-key-here" # Important: Change this!
        ACCESS_TOKEN_EXPIRE_MINUTES=30
        PYTHONUNBUFFERED=1
        ```

    *   **Content Service (`services/content-service/.env`):**
        Copy `services/content-service/.env.example` to `services/content-service/.env`.
        The `DATABASE_URL` should be:
        `DATABASE_URL="postgresql://content_user:content_password@content-db:5432/content_db"`
        ```env
        # services/content-service/.env
        DATABASE_URL="postgresql://content_user:content_password@content-db:5432/content_db"
        PYTHONUNBUFFERED=1
        ```

    *   **Suggestion Service (`services/suggestion-service/.env`):**
        Copy `services/suggestion-service/.env.example` to `services/suggestion-service/.env` or create it.
        This service currently doesn't require specific environment variables for its mock implementation, but `PYTHONUNBUFFERED=1` is good for logging.
        ```env
        # services/suggestion-service/.env
        PYTHONUNBUFFERED=1
        # Add other variables here if the service evolves (e.g., API keys for external AI models)
        ```

    **Note on `.env` files:** The `docker-compose.yml` file is configured to use these `.env` files. The database credentials (`auth_user`, `auth_password`, `content_user`, `content_password`) used in the `DATABASE_URL`s must match the `POSTGRES_USER` and `POSTGRES_PASSWORD` environment variables defined for the `auth-db` and `content-db` services in `docker-compose.yml`.

3.  **Build and Run the Application:**
    Open your terminal in the project root directory (where `docker-compose.yml` is located) and run:
    ```bash
    docker-compose up --build -d
    ```
    *   `--build`: Forces Docker Compose to rebuild the images if there are any changes in the Dockerfiles or application code.
    *   `-d`: Runs the containers in detached mode (in the background).

4.  **Accessing the Application:**

    *   **Frontend Application**:
        Once all services are up and running (check `docker-compose ps` or `docker ps`), you can access the frontend application through the Nginx gateway:
        *   URL: `http://localhost` (or `http://localhost:80`)

    *   **Backend Services (Direct Access - primarily for development/debugging):**
        The backend services are also mapped to specific ports on your host machine:
        *   Auth Service: `http://localhost:8001`
        *   Content Service: `http://localhost:8002`
        *   Suggestion Service: `http://localhost:8003`
        You can typically access their root endpoints (e.g., `http://localhost:8001/`) or health check endpoints to see if they are running. API interactions are intended to go through the gateway (e.g., `http://localhost/api/auth/...`).

    *   **Admin UI (if applicable):**
        If any of the services expose an admin UI (e.g., FastAPI's `/docs` for OpenAPI), you would access it via the gateway:
        *   Auth Service API Docs: `http://localhost/api/auth/docs`
        *   Content Service API Docs: `http://localhost/api/content/docs`
        *   Suggestion Service API Docs: `http://localhost/api/suggestions/docs`

5.  **Stopping the Application:**
    To stop all running containers, run:
    ```bash
    docker-compose down
    ```
    To stop and remove volumes (useful for a clean restart, **will delete database data**):
    ```bash
    docker-compose down -v
    ```

## Example `.env` Structure (Summary)

This is a summary of the key environment variables needed for local development:

*   **`services/auth-service/.env`**:
    ```
    DATABASE_URL="postgresql://auth_user:auth_password@auth-db:5432/auth_db"
    SECRET_KEY="a_very_secure_secret_key_that_you_must_change"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    PYTHONUNBUFFERED=1
    ```

*   **`services/content-service/.env`**:
    ```
    DATABASE_URL="postgresql://content_user:content_password@content-db:5432/content_db"
    PYTHONUNBUFFERED=1
    ```

*   **`services/suggestion-service/.env`**:
    ```
    PYTHONUNBUFFERED=1
    # OPENAI_API_KEY="your_optional_api_key"
    ```

## Optional: Simulating the AI Suggestion Engine

The `suggestion-service` currently provides mock/simulated suggestions. It does not integrate with a real AI/ML model.

*   **How it works**: The `services/suggestion-service/main.py` file contains a list of predefined content items and randomly selects a few to return as suggestions.
*   **Customization**: You can modify the `simulated_content_items` list in `services/suggestion-service/main.py` to change the pool of items from which suggestions are drawn.
*   **Future Integration**: To integrate a real AI model, you would typically:
    1.  Modify the suggestion service to call an external AI API or load a local model.
    2.  Add necessary environment variables (e.g., API keys, model paths) to `services/suggestion-service/.env` and configure the service to use them.
    3.  Update the service's Dockerfile if new dependencies are required for the AI model.

---

Happy Hacking!
```
