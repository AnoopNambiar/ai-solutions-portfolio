pipeline {

    agent any

    environment {
        APP_NAME   = "nasa-app"
        REGISTRY   = "localhost:5000"
        IMAGE      = "nasa-app:1.0"
        PYTHON     = ".venv/Scripts/python.exe"
    }

    stages {

        /*
         * ==========================================================
         * ENVIRONMENT CHECK
         * ==========================================================
         */
        stage('Environment Check') {
            steps {
                sh '''
                    echo "=========================================="
                    echo "Environment Check"
                    echo "=========================================="

                    python --version
                    where python

                    docker --version
                    trivy --version
                '''
            }
        }


        /*
         * ==========================================================
         * SETUP PYTHON ENVIRONMENT
         * ==========================================================
         */
        stage('Setup Python Environment') {
            steps {
                sh '''
                    echo "Creating Python virtual environment..."

                    python -m venv .venv

                    echo "Upgrading pip..."

                    .venv/Scripts/python.exe -m pip install --upgrade pip

                    echo "Installing application dependencies..."

                    .venv/Scripts/python.exe -m pip install -r requirements.txt

                    echo "Installing development dependencies..."

                    .venv/Scripts/python.exe -m pip install -r requirements-dev.txt
                '''
            }
        }


        /*
         * ==========================================================
         * STAGE A - CODE LINTING
         * ==========================================================
         */
        stage('A - Code Linting') {
            steps {

                echo 'Running Flake8...'

                sh '''
                    .venv/Scripts/python.exe -m flake8 .
                '''

                echo 'Checking Black formatting...'

                sh '''
                    .venv/Scripts/python.exe -m black --check .
                '''
            }
        }


        /*
         * ==========================================================
         * STAGE B - UNIT TESTING
         * ==========================================================
         */
        stage('B - Unit Testing') {
            steps {

                echo 'Running pytest...'

                sh '''
                    .venv/Scripts/python.exe -m pytest -v
                '''
            }
        }


        /*
         * ==========================================================
         * STAGE C - VULNERABILITY SCANNING
         *
         * 1. Scan source/dependencies
         * 2. Build Docker image
         * 3. Scan Docker image layers
         *
         * Pipeline stops if vulnerabilities are found.
         * ==========================================================
         */
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


                echo 'Building Docker image...'

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

                echo '=========================================='
                echo 'Vulnerability scan PASSED'
                echo '=========================================='
            }
        }


        /*
         * ==========================================================
         * STAGE D - PUSH TO LOCAL REGISTRY
         *
         * This stage executes ONLY if Stage C passes.
         * ==========================================================
         */
        stage('D - Push to Local Registry') {
            steps {

                echo 'Pushing security-approved Docker image...'

                sh '''
                    docker push "$IMAGE"
                '''

                echo '=========================================='
                echo 'Docker image pushed successfully'
                echo '=========================================='

                echo "Image: ${IMAGE}"
            }
        }
    }


    /*
     * ==========================================================
     * POST ACTIONS
     * ==========================================================
     */
    post {

        success {
            echo '=========================================='
            echo 'PIPELINE SUCCESSFUL'
            echo '=========================================='
            echo "Image: ${IMAGE}"
        }

        failure {
            echo '=========================================='
            echo 'PIPELINE FAILED'
            echo '=========================================='
            echo 'Security gate or another stage failed.'
            echo 'Docker image was NOT pushed.'
        }

        always {
            echo 'Cleaning temporary Python environment...'

            sh '''
                if [ -d ".venv" ]; then
                    rm -rf .venv
                fi
            '''
        }
    }
}