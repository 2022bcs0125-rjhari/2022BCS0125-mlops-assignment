pipeline {
    agent any
    environment {
        AWS_KEY_ID = 'ASIA5CKZFZM4ACLLZ4Z2'
        AWS_SECRET_KEY = 'QivLK43fGa/iC7i8NuMBcPPM+q9gmHM9nxLVSZCA'
        AWS_SESSION_TOK = 'IQoJb3JpZ2luX2VjEHAaCXVzLXdlc3QtMiJHMEUCIQCwu5YxcItJE9a7nCyKJFmrFaZ5c2HCqbU+iuOqXoxTNAIgLMPWMzuqqLxjNXQYxDJqM+tnbP0ox22x8eJzDj3Y8hAquQIIORAAGgw4OTgzNzIwNjIwMDgiDFPsyBtIvbbs3FjXDCqWAgp2/IJRg9iFM++bJDkXXM6Pz8ZuY0sWqgj5biJyzHPpztNs4xo0rSeme8Q2VbOLBcjSA44Az2S/WY5SfEiBm42NNJP6kTKr/EESTOropC9oi8XCv/f1+FagaSIPzLw5DojVKxxK1DmDjpXLMdx9ak1XmObtpdzPWIEuElWnnfbAGBg319O79Yavt+Mw5jzbnofwxo4s7VOzCn+2gIu8Pqaztfp1tAPklfotwe5yhGZkD0Fg19ipbXth9AuwX/ZKGVH9WVUerw7uMESi/wVpChDwthABXhwnu7e7bd4rj3ZvpB5AS8nx5OjVOo7g2dH6kFborbJ20ubV3F+83e7ehL9U+3x/12Px5HwRRd0Foy6eQZWJZ8IyMOyBrs4GOp0B0Q0qsGNwcUWe5kSs1nmvVmzNvL+f8sWQLMFaq0zJ6VwEk/qzwXU0eCiKcjbY0iPCyJVH3zPaV5EpBkmeghhivXABwuqGu7DywzgeTInysvgHZj0bQCnl739ETxOxlDTOa4mCsx04105+bVW/RO8Yn0AxfILt0VzriK0Ez0oMorwHmVIFehLoV9/ZKxY7SZddQ5K/HSWsR2ytITesEw=='
        AWS_DEFAULT_REGION = 'us-east-1'
    }


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
                echo "Checking AWS..."
                echo $AWS_KEY_ID

                . venv/bin/activate

                dvc pull -v
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