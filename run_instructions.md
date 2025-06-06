# Running and Visualizing the Application

This guide explains how to set up and run the Intelligent Stock Management System locally using Docker Compose, and how to access its different interfaces.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker**: For running the application containers. [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: Usually included with Docker Desktop. If not, [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Git**: For cloning the repository (if you haven't already).
- **Web Browser**: Chrome, Firefox, Edge, etc.

## Setup and Running with Docker Compose (Recommended)

Using Docker Compose is the easiest way to get the entire application stack (frontend, backend, database) running with a single command.

1.  **Clone the Repository** (if you haven't):
    ```bash
    git clone <your-repository-url>
    cd intelligent-stock-system
    ```

2.  **Configure Environment Variables**:
    -   Navigate to the `backend/` directory.
    -   Copy the `.env.example` file to `.env`:
        ```bash
        cp backend/.env.example backend/.env
        ```
    -   **Edit `backend/.env`**: Fill in the required values, especially:
        -   `DATABASE_URL`: Should match the Docker Compose database service (e.g., `postgresql://postgres:password@db:5432/stock_management` - the default in `docker-compose.yml` should work).
        -   `SECRET_KEY`: Generate a strong secret key.
        -   `DYNAMICS_BC_*`: **Crucially, provide your actual Microsoft Dynamics 365 Business Central API credentials.** Without these, the BC integration will not work.

3.  **Build and Start Containers**:
    -   From the **root directory** of the project (`intelligent-stock-system/`), run:
        ```bash
        docker-compose up --build -d
        ```
    -   `--build`: Forces Docker to rebuild the images if the code has changed.
    -   `-d`: Runs the containers in detached mode (in the background).
    -   This command will:
        -   Build the Docker images for the `frontend` and `backend` services.
        -   Pull the `postgres:14` image for the database.
        -   Create and start containers for all three services.
        -   Set up the necessary network connections between containers.

4.  **Database Migrations (First Time)**:
    -   Once the containers are running, you need to apply the database migrations using Alembic. Run this command from the root directory:
        ```bash
        docker-compose exec backend alembic upgrade head
        ```
    -   This executes the `alembic upgrade head` command inside the running `backend` container.

5.  **Accessing the Application**:
    -   **Frontend UI**: Open your web browser and navigate to:
        [http://localhost:3000](http://localhost:3000)
    -   **Backend API Documentation (Swagger UI)**: Open your web browser and navigate to:
        [http://localhost:8000/docs](http://localhost:8000/docs)
        Here you can explore and interact with the backend API endpoints directly.

6.  **Stopping the Application**:
    -   To stop the running containers, run from the root directory:
        ```bash
        docker-compose down
        ```
    -   To stop and remove the data volume (use with caution, deletes database data):
        ```bash
        docker-compose down -v
        ```

## Manual Setup (Without Docker)

Running manually requires setting up the database, backend, and frontend separately.

1.  **Database Setup**:
    -   Install PostgreSQL locally.
    -   Create a database (e.g., `stock_management`) and a user/password.
    -   Update the `DATABASE_URL` in `backend/.env` accordingly.
    -   Run migrations: `cd backend && source venv/bin/activate && alembic upgrade head`

2.  **Backend Setup**:
    -   Navigate to the `backend/` directory.
    -   Create and activate a Python virtual environment: `python -m venv venv && source venv/bin/activate`
    -   Install dependencies: `pip install -r requirements.txt`
    -   Ensure the `.env` file is configured correctly (especially `DATABASE_URL` and `DYNAMICS_BC_*` credentials).
    -   Run the backend server: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

3.  **Frontend Setup**:
    -   Navigate to the `frontend/` directory.
    -   Install Node.js and npm/yarn if you haven't already.
    -   Install dependencies: `npm install` (or `yarn install`)
    -   Run the frontend development server: `npm run dev` (or `yarn dev`)

4.  **Accessing the Application**:
    -   Frontend UI: [http://localhost:5173](http://localhost:5173) (Vite's default port, check console output)
    -   Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Visualization

-   **Frontend Dashboard**: The primary way to visualize data (stock levels, forecasts, alerts) is through the React frontend application running at `http://localhost:3000` (Docker) or `http://localhost:5173` (Manual).
-   **API Interaction**: You can use the Swagger UI at `http://localhost:8000/docs` to send requests to the backend and see the raw JSON responses, which can be useful for debugging or direct data inspection.
-   **Database**: You can connect to the PostgreSQL database directly using tools like `psql`, pgAdmin, or DBeaver to inspect the raw data in the tables. (Connect to `localhost:5432` with user `postgres`, password `password`, database `stock_management` if using Docker defaults).
