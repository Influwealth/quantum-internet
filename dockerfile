# Use a stable version of Python
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the new requirements file and install the correct libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# The command to start your agent server
CMD ["uvicorn", "mesh_server:app", "--host", "0.0.0.0", "--port", "10000"]
