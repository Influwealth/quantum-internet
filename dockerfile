# Use a stable version of Python
FROM python:3.11-slim

# Install the Rust compiler and its tools (the "welding equipment")
RUN apt-get update && apt-get install -y curl && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install the Python libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# The command to start your server
CMD ["uvicorn", "mesh_server:app", "--host", "0.0.0.0", "--port", "10000"]
