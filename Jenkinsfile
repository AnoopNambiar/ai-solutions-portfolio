pipeline {

    agent any

    environment {
        APP_NAME   = "nasa-app"
        REGISTRY   = "localhost:5000"
        IMAGE      = "nasa-app:1.0"
    }

    stages {

        stage('A - Code Linting') {
            steps {
                echo 'Running Flake8...'

                sh '''
                    python3 -m flake8 .
                '''

                echo 'Checking Black formatting...'

                sh '''
                    python3 -m black --check .
                '''
            }
        }

        stage('B - Unit Testing') {
            steps {
                echo 'Installing dependencies...'

                sh '''
                    python3 -m pip install -r requirements.txt
                    python3 -m pip install -r requirements-dev.txt
                '''

                echo 'Running pytest...'

                sh '''
                    python3 -m pytest -v
                '''
            }
        }

        stage('C - Vulnerability Scan') {
            steps {

                echo 'Scanning project dependencies with Trivy...'

                sh '''
                    trivy fs \
                      --scanners vuln \
                      --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
                      --exit-code 1 \
                      .
                '''

                echo 'Building Docker image for security scanning...'

                sh '''
                    docker build \
                      -t "$IMAGE" \
                      .
                '''

                echo 'Scanning Docker image with Trivy...'

                sh '''
                    trivy image \
                      --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
                      --exit-code 1 \
                      "$IMAGE"
                '''

                echo 'Vulnerability scan passed.'
            }
        }

        stage('D - Push to Local Registry') {
            steps {

                echo 'Pushing security-approved image...'

                sh '''
                    docker push "$IMAGE"
                '''

                echo "Image pushed successfully: ${IMAGE}"
            }
        }
    }

    post {

        success {
            echo '=============================================='
            echo 'PIPELINE SUCCESSFUL'
            echo '=============================================='
            echo "Docker image: ${IMAGE}"
        }

        failure {
            echo '=============================================='
            echo 'PIPELINE FAILED'
            echo '=============================================='
            echo 'Build stopped. Image was NOT pushed.'
        }
    }
}