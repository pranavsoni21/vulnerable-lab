# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Initialize the DB
RUN python db_init.py

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
