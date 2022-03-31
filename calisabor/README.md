# Cali Sabor API

This app is created for Productos y Condimentos Cali Sabor (CS) to manage and administrate marketing for clients.
Also, we can manage inventory for the client venues and in our own warehouse.

## Requirements

- Docker
- Mongo:4.0.8

## Installation

- [Windows Guide](https://docs.docker.com/desktop/windows/install/)
- [Mag Guide](https://docs.docker.com/desktop/mac/install/)
- [Linux Guide](https://docs.docker.com/engine/install/)

## Run Database
To create the database we are going to use official mongo image from dockerhub, and using the next command we can create a new database with access credentials to work in project.
```
user@network$ docker run -d -p 0.0.0.0:27017:27017 --name calisabordb -v ~/apps/cs_db:/data/db -e MONGO_INITDB_ROOT_USERNAME=cs_admin -e MONGO_INITDB_ROOT_PASSWORD=p445w0rd mongo:4.0.8
```
## Run API
To create this app we are using an image located in Dockerhub, and using the next code after the database is running creates the CS_API service using docker.
```
user@network$ docker run -d luanvarmo/cs_login:latest
```

