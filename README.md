# Cali Sabor APP

This app is created by Luica and Neo Software company for Productos y Condimentos Cali Sabor.

### Start Backend services

Clone repository and go inside the directory
```
git clone https://github.com/Cali-Sabor/CaliSaborAPI.git
```
Go inside this new directory
```
cd CaliSaborAPI
```
Then change branch to develop
```
git checkout develop
```
Once inside the root directory of API on develop branch, write the following command to build and up the services (mongo database and API service)
```
docker-compose up --build -d
```
When services is running try to log in using your preference tool (postman, insomnia) to make request and check connection.

