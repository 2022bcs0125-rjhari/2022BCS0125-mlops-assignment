pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        AWS_DEFAULT_REGION = 'ap-south-1'
    }

    stages {

        stage('Clone Repo') {
            steps {
                git 'https://github.com/your-username/your-repo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('DVC Pull') {
            steps {
                sh '''
                . venv/bin/activate
                dvc pull
                '''
            }
        }

        stage('Train Model + MLflow') {
            steps {
                sh '''
                . venv/bin/activate
                python src/train.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t yourusername/2022bcs0125-mlops .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push yourusername/2022bcs0125-mlops
                    '''
                }
            }
        }
    }
}