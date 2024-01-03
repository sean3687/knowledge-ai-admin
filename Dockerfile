# Use a specific version of Python image for consistency
FROM python:3.8-slim

# Install dependencies required for building Python packages
RUN apt-get update && apt-get install -y gcc libpq-dev

# Using a non-root user for better security
RUN useradd -m myuser
USER myuser

# Set an environment variable to store the directory where the app is installed
ENV APP_HOME=/home/myuser/app
WORKDIR $APP_HOME

# Your existing steps to copy requirements and install
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
