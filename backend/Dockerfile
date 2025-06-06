FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed (e.g., for specific libraries)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY alembic.ini .

# Expose the port the app runs on
EXPOSE 8000

# Set environment variables (can be overridden in docker-compose)
# ENV DATABASE_URL=postgresql://user:password@db:5432/stock_management
# ENV SECRET_KEY=your-default-secret-key

# Run database migrations (optional, can be done manually after container starts)
# RUN alembic upgrade head

# Command to run the application using uvicorn
# Use --host 0.0.0.0 to make it accessible outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

