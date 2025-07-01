# Use a stable version of Python
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file (we will create this next)
COPY requirements.txt .

# Install all the necessary tools
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# The command to start your server
CMD ["uvicorn", "mesh_server:app", "--host", "0.0.0.0", "--port", "10000"]
