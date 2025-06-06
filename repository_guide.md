# Repository Structure and File Guide

This guide explains the structure of the `intelligent-stock-system` repository, detailing the purpose of key directories and files within both the frontend and backend components.

## Top-Level Structure

The repository follows a monorepo structure, containing both the frontend and backend code in separate directories:

```
intelligent-stock-system/
├── frontend/         # React frontend application
├── backend/          # FastAPI backend application
├── docker-compose.yml # Docker configuration for running both services
└── README.md         # Main project README
```

- **`frontend/`**: Contains the user interface code built with React and TypeScript.
- **`backend/`**: Contains the server-side logic, API, database interactions, and AI forecasting code built with FastAPI (Python).
- **`docker-compose.yml`**: Defines the services (backend, frontend, database) for easy local development setup using Docker.
- **`README.md`**: Provides an overview of the project, setup instructions, and other relevant information.

## Frontend Directory (`frontend/`)

This directory contains the React application built using Vite and TypeScript, styled with Tailwind CSS and Shadcn/UI components.

```
frontend/
├── public/             # Static assets (e.g., index.html base, favicons)
├── src/
│   ├── App.tsx           # Main application component, routing setup
│   ├── index.css         # Global CSS styles (Tailwind base)
│   ├── index.tsx         # Entry point for the React application
│   ├── components/       # Reusable UI components
│   │   └── ui/           # Shadcn/UI components
│   ├── contexts/         # React context providers (e.g., AuthContext)
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utility functions (e.g., cn for classnames)
│   ├── pages/            # Page-level components (routed views)
│   ├── services/         # API interaction logic (e.g., api.ts)
│   └── types/            # TypeScript type definitions
├── .env.example        # Example environment variables
├── .gitignore          # Specifies intentionally untracked files
├── index.html          # HTML entry point for Vite
├── package.json        # Project dependencies and scripts
├── tailwind.config.ts  # Tailwind CSS configuration
├── tsconfig.json       # TypeScript compiler configuration
└── vite.config.ts      # Vite build tool configuration
```

- **`src/`**: The core source code of the frontend application.
- **`src/components/`**: Contains reusable UI elements. `ui/` specifically holds the Shadcn/UI components.
- **`src/contexts/`**: Manages global state using React Context (e.g., authentication status).
- **`src/hooks/`**: Custom hooks for encapsulating reusable logic.
- **`src/lib/`**: General utility functions.
- **`src/pages/`**: Components representing distinct pages or views of the application.
- **`src/services/`**: Modules responsible for making API calls to the backend.
- **`src/types/`**: Shared TypeScript interfaces and types.
- **`package.json`**: Lists frontend dependencies (React, Tailwind, Shadcn/UI, etc.) and defines scripts (`dev`, `build`).
- **`vite.config.ts`**: Configuration for the Vite development server and build process.

## Backend Directory (`backend/`)

This directory contains the FastAPI application responsible for handling business logic, API requests, database operations, and AI forecasting.

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py        # Aggregates all v1 API routers
│   │       ├── deps.py       # API dependencies (e.g., get_db, get_current_user)
│   │       └── endpoints/    # Specific API endpoint logic
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── products.py
│   │           ├── sales.py
│   │           ├── forecasts.py
│   │           └── alerts.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py     # Application settings (from .env)
│   │   └── security.py   # Password hashing, token creation
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py       # SQLAlchemy Base class
│   │   ├── session.py    # Database session management
│   │   └── models/       # SQLAlchemy ORM models
│   │       ├── __init__.py
│   │       ├── user.py
│   │       ├── product.py
│   │       ├── sales.py
│   │       ├── forecast.py
│   │       └── alert.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py       # Pydantic schemas for User data
│   │   ├── product.py    # Pydantic schemas for Product data
│   │   ├── sales.py      # Pydantic schemas for Sales data
│   │   ├── forecast.py   # Pydantic schemas for Forecast data
│   │   ├── alert.py      # Pydantic schemas for Alert data
│   │   └── token.py      # Pydantic schemas for Token data
│   ├── services/
│   │   ├── __init__.py
│   │   ├── dynamics_bc.py # Service for Dynamics BC integration
│   │   ├── forecast.py    # Service for AI forecasting (Prophet)
│   │   └── notification.py # (Placeholder) Service for sending notifications
│   └── utils/
│       ├── __init__.py
│       └── helpers.py    # (Placeholder) Utility helper functions
├── alembic/              # Alembic database migration configuration
│   ├── versions/         # Alembic migration scripts
│   └── alembic.ini       # Alembic configuration file
├── tests/                # Unit and integration tests (Placeholder)
├── .env.example          # Example environment variables for backend
├── requirements.txt      # Python dependencies
└── Dockerfile            # Docker build instructions for the backend
```

- **`app/`**: Core application code.
- **`app/main.py`**: Creates the FastAPI app instance, includes routers, and configures middleware (like CORS).
- **`app/api/v1/`**: Contains version 1 of the API.
    - **`endpoints/`**: Defines the actual API routes (e.g., `/products`, `/auth/login`).
    - **`deps.py`**: FastAPI dependency functions for things like database sessions and user authentication.
- **`app/core/`**: Core application logic like settings management and security functions.
- **`app/db/`**: Database-related code.
    - **`models/`**: SQLAlchemy ORM classes representing database tables.
    - **`session.py`**: Logic for creating and managing database sessions.
- **`app/schemas/`**: Pydantic models used for data validation and serialization in API requests/responses.
- **`app/services/`**: Business logic layer, encapsulating interactions with external services (Dynamics BC) or complex operations (forecasting).
- **`alembic/`**: Directory for managing database schema migrations using Alembic.
- **`requirements.txt`**: Lists the Python packages required for the backend.
- **`Dockerfile`**: Instructions for building a Docker image for the backend service.
