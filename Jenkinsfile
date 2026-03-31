pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pip install awscli dvc[s3]
                '''
            }
        }

        stage('Configure AWS') {
            steps {
                sh '''
                mkdir -p ~/.aws

                cat <<EOF > ~/.aws/credentials
[default]
aws_access_key_id=YOUR_ACCESS_KEY
aws_secret_access_key=YOUR_SECRET_KEY
aws_session_token=YOUR_SESSION_TOKEN
EOF

                cat <<EOF > ~/.aws/config
[default]
region=us-east-1
EOF

                echo "AWS CONFIG:"
                cat ~/.aws/credentials
                cat ~/.aws/config
                '''
            }
        }

        stage('Test AWS Connection') {
            steps {
                sh '''
                . venv/bin/activate
                aws s3 ls s3://2022bcs0125-mlops-assignment
                '''
            }
        }

        stage('DVC Pull') {
            steps {
                sh '''
                . venv/bin/activate

                export AWS_EC2_METADATA_DISABLED=true
                export DVC_NO_ANALYTICS=1

                dvc pull --jobs 1 -v
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