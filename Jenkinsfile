pipeline {
    agent any

    stages {
        stage('Install docker-compose') {
        steps {
            sh 'curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
            sh 'curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
            sh 'chmod +x /usr/local/bin/docker-compose'
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose up -d --build'
            }
        }
    }
}

