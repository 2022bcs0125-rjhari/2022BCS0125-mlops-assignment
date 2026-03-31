pipeline {
    agent any


    stages {


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
        withCredentials([
            string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
            string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY'),
            string(credentialsId: 'aws-session-token', variable: 'AWS_SESSION_TOKEN')
        ]) {
            sh '''
            echo "Setting AWS manually..."

            mkdir -p ~/.aws

            echo "[default]" > ~/.aws/credentials
            echo "aws_access_key_id=$AWS_ACCESS_KEY_ID" >> ~/.aws/credentials
            echo "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" >> ~/.aws/credentials
            echo "aws_session_token=$AWS_SESSION_TOKEN" >> ~/.aws/credentials

            echo "[default]" > ~/.aws/config
            echo "region=us-east-1" >> ~/.aws/config

            cat ~/.aws/credentials
            cat ~/.aws/config

            . venv/bin/activate

            dvc pull -v
            '''
        }
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