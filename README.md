# Intelligent Stock Management System

This project is a full-stack application designed for intelligent stock management, featuring sales forecasting and integration with Microsoft Dynamics 365 Business Central.

## Features

*   **Product Management:** CRUD operations for managing product details and stock levels.
*   **Sales Data Handling:** Import sales data from Dynamics BC and store raw/cleaned versions.
*   **AI-Powered Forecasting:** Utilizes Prophet time-series forecasting to predict future sales demand based on historical data.
*   **Stock Alerting:** Generates alerts when forecasted stock levels fall below defined reorder thresholds.
*   **Dynamics BC Integration:** Connects to Dynamics BC API to fetch item data and sales ledger entries.
*   **User Authentication:** Secure login and registration using JWT.
*   **Modern Frontend:** Responsive user interface built with React, TypeScript, and Tailwind CSS.
*   **Robust Backend:** API built with FastAPI (Python) and SQLAlchemy for database interaction.
*   **Containerized Deployment:** Dockerized setup using Docker Compose for easy local development and deployment.

## Technology Stack

*   **Frontend:** React, TypeScript, Vite, Tailwind CSS, Shadcn/UI
*   **Backend:** Python, FastAPI, SQLAlchemy, Pydantic
*   **Database:** PostgreSQL
*   **Forecasting:** Prophet (by Meta)
*   **API Integration:** Python `requests` library (for Dynamics BC)
*   **Containerization:** Docker, Docker Compose
*   **Database Migrations:** Alembic

## Project Structure

```
/
├── backend/          # FastAPI backend application
│   ├── app/            # Core backend code (API, DB, services, etc.)
│   ├── alembic/        # Database migrations
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/         # React frontend application
│   ├── src/            # Core frontend code (components, pages, services)
│   ├── public/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml # Docker Compose configuration
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

*(Refer to `repository_guide.md` for a more detailed breakdown)*

## Getting Started

### Prerequisites

*   Docker & Docker Compose
*   Git
*   Node.js & npm/yarn (for frontend development outside Docker)
*   Python 3.9+ (for backend development outside Docker)
*   Access credentials for Microsoft Dynamics 365 Business Central API

### Running with Docker (Recommended)

1.  **Clone the repository** (if you haven't already).
2.  **Configure Backend Environment:**
    *   Navigate to the `backend/` directory.
    *   Copy `.env.example` to `.env`: `cp .env.example .env`
    *   Edit `backend/.env` and fill in your `SECRET_KEY`, `DATABASE_URL` (usually defaults are fine for Docker), and **crucially, your Dynamics BC API credentials** (`DYNAMICS_BC_*` variables).
3.  **Build and Start Containers:** From the project root directory, run:
    ```bash
    docker-compose up --build -d
    ```
4.  **Apply Database Migrations (First Run):**
    ```bash
    docker-compose exec backend alembic upgrade head
    ```
5.  **Access the Application:**
    *   Frontend: `http://localhost:5173` (or the port mapped in `docker-compose.yml` for the frontend service)
    *   Backend API Docs: `http://localhost:8000/docs`

*(Refer to `run_instructions.md` or `mac_developer_guide.md` for more detailed setup and development instructions)*

## Usage

1.  **Register/Login:** Access the frontend UI and create an account or log in.
2.  **Manage Products:** Add or update product information, including stock levels and reorder thresholds.
3.  **Import Sales Data:** Use the UI or API to trigger the import of sales data from Dynamics BC for relevant products and date ranges.
4.  **Generate Forecasts:** Trigger the forecast generation process via the UI or API. This will use the cleaned sales data to predict future demand.
5.  **View Forecasts & Alerts:** Check the dashboard or relevant sections for sales forecasts and any generated low-stock alerts.

## Contributing

Contributions are welcome! Please follow standard Git workflow (fork, branch, pull request).