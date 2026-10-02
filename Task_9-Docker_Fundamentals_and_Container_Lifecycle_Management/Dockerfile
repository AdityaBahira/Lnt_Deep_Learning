# Step 1: Use official lightweight Python base image
FROM python:3.10-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DATA_DIR=/app/data

# Step 4: Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy application source code
COPY app.py .

# Step 6: Expose container port
EXPOSE 5000

# Step 7: Define volume mount point
VOLUME ["/app/data"]

# Step 8: Specify container execution entrypoint
CMD ["python", "app.py"]
