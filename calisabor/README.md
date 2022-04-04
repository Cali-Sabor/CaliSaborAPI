# Cali Sabor API

This app is created for Productos y Condimentos Cali Sabor (CS) to manage and administrate marketing for clients.
Also, we can manage inventory for the client venues and in our own warehouse.

## Requirements

- Docker
- Mongo:4.0.8
- PowerShell (Windows)

## Installation

- [Windows Guide](https://docs.docker.com/desktop/windows/install/)
- [Mag Guide](https://docs.docker.com/desktop/mac/install/)
- [Linux Guide](https://docs.docker.com/engine/install/)

## Run Database
To create the database we are going to use official mongo image from dockerhub, and using the next command (powershell or console) we can create a new database with access credentials to work in project.
#### Linux
```
docker run -d -p 0.0.0.0:27017:27017 --name calisabordb -v ~/apps/cs_db:/data/db -e MONGO_INITDB_ROOT_USERNAME=cs_admin -e MONGO_INITDB_ROOT_PASSWORD=p445w0rd mongo:4.0.8
```
#### Windows
```
docker run -d -p 0.0.0.0:27017:27017 --name calisabordb -v /app/cs_db:/data/db -e MONGO_INITDB_ROOT_USERNAME=cs_admin -e MONGO_INITDB_ROOT_PASSWORD=p445w0rd mongo:4.0.8
```
## Run API
To create this app we are using an image located in Dockerhub, and using the next code after the database is running creates the CS_API service using docker.

First, download de image:
```
docker pull luanvarmo/cs_login:latest
```
Then, install:
```
docker run -d -p 8000:8000 luanvarmo/cs_login:latest
```

Be careful, if you don't run the database script first before this script, you will get an error.
