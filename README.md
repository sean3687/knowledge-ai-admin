
# CPAL-admin-backend

This is separate backend service from chitchatrabbit. 

# How to run Docker container locally

This project is running in docker container. 

**Step 1: Clone this repository**

```
git clone https://github.com/sean3687/knowledge-ai-admin.git
``` 

**Step 2: Download Docker desktop**

In order to run this backend locally please download docker desktop first:('https://www.docker.com/')

**Step 3: Build Docker image**

It's a good practice to run docker-compose build whenever you make changes to the Dockerfile or need to update the images as per the latest application code or dependencies

```
docker compose build
```

**Step 4 : Now run Docker**

You can access Fast API swagger in http://localhost:8000/docs

```
docker compose up
```

# pgAdmin - Access postgre 13 database

Once you run container with docker compose, it automatically run pg admin and database together. You can access database within pgAdmin

**Step 1: Open pgAdmin in web**

Your pgAdmin is running on http://locahost:5050
- PGADMIN_DEFAULT_EMAIL: yonghyun.jin11@gmail.com 
- PGADMIN_DEFAULT_PASSWORD: sean0305.

**Step 2: Connect database server**

Go to the 'Connection' tab, and enter the following details:
- Host name/address: localhost (since your database container is mapped to your host's port 5432)
- Port: 5432 (as specified in your configuration)
- Maintenance database: admin-db (as per your POSTGRES_DB environment variable)
- Username: admin (as per your POSTGRES_USER environment variable)
- Password: sean0305 (as per your POSTGRES_PASSWORD environment variable)


# Merge Guideline

Please create your own branch when you work on the project.

# Deployment server

Within .pem, file you can access to AWS ec2 instance. In the terminal, go to where .pem file is located through your terminal

```
ssh -i "cpal-backend-admin.pem" ubuntu@ec2-13-57-49-216.us-west-1.compute.amazonaws.com
```


In order to check what containers are running, run following command:
```
docker ps
```

# Push to deployment server

**Pull the Latest Code**:

- First, ensure that the latest version of your code is available on the server. If your code is in a Git repository, you can use **`git pull`** to fetch the latest changes.

**Rebuild the Docker Image**:
- Navigate to the directory where your Dockerfile is located.
- Rebuild the image. This step assumes that your Docker Compose setup builds the image from a Dockerfile. Run:
        
    ```
    docker-compose build web
    ```    
  
        
    - This command rebuilds the image for the **`web`** service defined in your **`docker-compose.yml`**.

**Stop the Running Containers**:
- It's good practice to stop the running containers before starting them again with the updated configuration. Run:
    ```
    docker-compose down
    ```

        
**Start the Containers with the Updated Configuration**:
- Now, start the containers again with the updated configuration. Run:    
    ```
    docker-compose up -d
    ```
        
- This command will start all the services defined in your 
`docker-compose.yml`** file, including your updated **`web`** service.
