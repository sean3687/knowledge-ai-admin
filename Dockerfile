# Assuming you're using a Python-based image
FROM python:3.8

# Update and install necessary dependencies
RUN apt-get update && apt-get install -y gcc python3-dev

# If you still face issues related to missing headers
# RUN apt-get install -y linux-headers-$(uname -r)

# Your existing steps to copy requirements and install
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
