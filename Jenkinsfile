pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = 'ASIA5CKZFZM4ACLLZ4Z2'
        AWS_SECRET_ACCESS_KEY = 'QivLK43fGa/iC7i8NuMBcPPM+q9gmHM9nxLVSZCA'
        AWS_DEFAULT_REGION = 'us-east-1'
    }

    stages {

        stage('Clone Repo') {
            steps {
                git 'https://github.com/2022bcs0125-rjhari/2022BCS0125-mlops-assignment.git'
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