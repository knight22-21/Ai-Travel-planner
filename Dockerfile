# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app/backend

# Copy only requirements first
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Set working directory to where main.py lives
WORKDIR /app/backend/backend

# Add project folder to PYTHONPATH so internal modules can be found
ENV PYTHONPATH=/app/backend/backend

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
