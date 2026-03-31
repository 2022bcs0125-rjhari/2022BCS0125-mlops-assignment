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
            string(credentialsId: 'aws-access-key-id', variable: 'ACCESS'),
            string(credentialsId: 'aws-secret-access-key', variable: 'SECRET'),
            string(credentialsId: 'aws-session-token', variable: 'TOKEN')
        ]) {
            sh '''
            echo "CHECKING..."

            echo "ACCESS=$ACCESS"
            echo "SECRET=$SECRET"
            echo "TOKEN=$TOKEN"

            export AWS_ACCESS_KEY_ID=$ACCESS
            export AWS_SECRET_ACCESS_KEY=$SECRET
            export AWS_SESSION_TOKEN=$TOKEN
            export AWS_DEFAULT_REGION=us-east-1

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