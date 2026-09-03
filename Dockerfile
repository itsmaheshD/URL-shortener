# Use lightweight Python image
FROM python:3.14-slim

# Set working directory inside the container
WORKDIR /app

# Install UV package manager
RUN pip install --no-cache-dir uv

# Copy dependency files first so Docker can cache dependency installation
COPY pyproject.toml uv.lock ./

# Install project dependencies from the lock file
RUN uv sync --frozen

# Copy application source code
COPY src ./src

# Copy Alembic configuration and migration files
COPY alembic.ini ./
COPY migrations ./migrations

# Tell Python where the application package lives
ENV PYTHONPATH=/app/src

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI application
CMD ["uv", "run", "uvicorn", "url_designer.main:app", "--host", "0.0.0.0", "--port", "8000"]