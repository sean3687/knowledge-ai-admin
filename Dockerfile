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

# Copy the requirements.txt first to leverage Docker cache
COPY requirements.txt $APP_HOME/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at $APP_HOME
COPY . $APP_HOME/

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
