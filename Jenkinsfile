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
        sh '''
        . venv/bin/activate

        export AWS_ACCESS_KEY_ID='YOUR_KEY'
        export AWS_SECRET_ACCESS_KEY='YOUR_SECRET'
        export AWS_SESSION_TOKEN='YOUR_TOKEN'
        export AWS_DEFAULT_REGION='us-east-1'

        # IMPORTANT FIX
        export AWS_EC2_METADATA_DISABLED=true
        export DVC_NO_ANALYTICS=1

        # Force sync (no async s3fs issues)
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
