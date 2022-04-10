#!groovy
pipeline {
    agent any

    stages {
        stage('Download docker') {
            steps {
                sh 'pip install docker'
            }
        }
        stage('Install and run database') {
            steps {
                sh 'docker run -d -p 0.0.0.0:27017:27017 --name calisabordb -v ~/apps/cs_db:/data/db -e MONGO_INITDB_ROOT_USERNAME=cs_admin -e MONGO_INITDB_ROOT_PASSWORD=p445w0rd mongo:4.0.8'
            }
        }
        stage('Build') {
            steps {
                echo 'ls'
                sh 'docker-compose up -d --build'
            }
        }
    }
}

