pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-key')
        AWS_SESSION_TOKEN = credentials('aws-session-token')

        DOCKER_ACCESS = credentials('docker-access')
        MLFLOW_TRACKING_URI = "http://localhost:5000"
        BUCKET_NAME = "2022bcs0125-mlops-assignment"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/2022bcs0125-rjhari/2022BCS0125-mlops-assignment.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                # Create a virtual environment
                python3 -m venv venv

                # Activate virtual environment
                . venv/bin/activate

                # Upgrade pip inside venv only
                pip install --upgrade pip

                # Install project dependencies
                pip install -r requirements.txt
                pip install mlflow boto3 dvc[s3] scikit-learn
                '''
            }
        }

        stage('Configure AWS') {
            steps {
                sh '''
                # Activate virtual environment
                . venv/bin/activate

                # Configure AWS CLI
                aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                aws configure set aws_session_token $AWS_SESSION_TOKEN
                aws configure set default.region us-east-1
                '''
            }
        }

        stage('Start MLflow') {
            steps {
                sh '''
                . venv/bin/activate
                export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                export AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN
                mlflow server \
                    --host 0.0.0.0 \
                    --port 5000 \
                    --backend-store-uri sqlite:///mlflow.db \
                    --default-artifact-root s3://2022bcs0125-mlops-assignment/ &
                sleep 5
                '''
            }
        }

        stage('Pull Data (DVC)') {
            steps {
                sh '''
                # Activate virtual environment
                . venv/bin/activate

                # Pull dataset from DVC
                dvc pull
                '''
            }
        }

        stage('Train Model + MLflow Logging') {
            steps {
                sh '''
                # Activate virtual environment
                . venv/bin/activate

                export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                export AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN
                export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI
                python src/train.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $DOCKER_ACCESS_USR/2022bcs0125-mlops-assignment .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                echo $DOCKER_ACCESS_PSW | docker login -u $DOCKER_ACCESS_USR --password-stdin
                docker push $DOCKER_ACCESS_USR/2022bcs0125-mlops-assignment
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed!"
        }
    }
}