pipeline {

    agent any

    environment {
        APP_NAME   = "nasa-app"
        REGISTRY   = "localhost:5000"
        IMAGE      = "nasa-app:1.0"

        PYTHON     = ".venv/Scripts/python.exe"
    }

    stages {

        // =====================================================
        // ENVIRONMENT CHECK
        // =====================================================

        stage('Environment Check') {
            steps {

                echo '=========================================='
                echo 'Environment Check'
                echo '=========================================='

                sh '''
                    echo "Python:"
                    python --version
                    where python

                    echo ""
                    echo "Docker:"
                    docker --version

                    echo ""
                    echo "Trivy:"
                    trivy --version
                '''
            }
        }


        // =====================================================
        // SETUP PYTHON VIRTUAL ENVIRONMENT
        // =====================================================

        stage('Setup Python Environment') {
            steps {

                echo '=========================================='
                echo 'Setup Python Environment'
                echo '=========================================='

                sh '''
                    echo "Creating Python virtual environment..."

                    python -m venv .venv

                    echo "Upgrading pip..."

                    .venv/Scripts/python.exe -m pip install --upgrade pip

                    echo "Installing application dependencies..."

                    .venv/Scripts/python.exe -m pip install -r requirements.txt

                    echo "Installing development dependencies..."

                    .venv/Scripts/python.exe -m pip install -r requirements-dev.txt

                    echo "Installed packages:"

                    .venv/Scripts/python.exe -m pip list
                '''
            }
        }


        // =====================================================
        // STAGE A - CODE LINTING
        // =====================================================

        stage('A - Code Linting') {
            steps {

                echo '=========================================='
                echo 'Stage A - Code Linting'
                echo '=========================================='

                echo 'Checking Flake8 installation...'

                sh '''
                    .venv/Scripts/python.exe -m flake8 --version
                '''

                echo 'Running Flake8...'

                sh '''
                    .venv/Scripts/python.exe -m flake8 *.py tests
                '''

                echo 'Checking Black installation...'

                sh '''
                    .venv/Scripts/python.exe -m black --version
                '''

                echo 'Running Black format check...'

                sh '''
                    .venv/Scripts/python.exe -m black --check *.py tests
                '''

                echo 'Code linting completed successfully.'
            }
        }


        // =====================================================
        // STAGE B - UNIT TESTING
        // =====================================================

        stage('B - Unit Testing') {
            steps {

                echo '=========================================='
                echo 'Stage B - Unit Testing'
                echo '=========================================='

                echo 'Checking pytest installation...'

                sh '''
                    .venv/Scripts/python.exe -m pytest --version
                '''

                echo 'Running unit tests...'

                sh '''
                    .venv/Scripts/python.exe -m pytest -v
                '''

                echo 'Unit testing completed successfully.'
            }
        }


        // =====================================================
        // DOCKER ENVIRONMENT CHECK
        // =====================================================

        stage('Docker Environment Check') {
            steps {

                echo '=========================================='
                echo 'Docker Environment Check'
                echo '=========================================='

                sh '''
                    echo "=== Docker Context ==="
                    docker context ls

                    echo "=== Docker Version ==="
                    docker version

                    echo "=== Docker Info ==="
                    docker info
                '''
            }
        }


        // =====================================================
        // STAGE C - VULNERABILITY SCAN
        // =====================================================

        stage('C - Vulnerability Scan') {
            steps {

                echo '=========================================='
                echo 'Stage C - Vulnerability Scan'
                echo '=========================================='


                // -------------------------------------------------
                // 1. FILESYSTEM / DEPENDENCY SCAN
                // -------------------------------------------------

                echo 'Scanning project dependencies with Trivy...'

                sh '''
                    trivy fs \
                        --scanners vuln \
                        --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
                        --exit-code 1 \
                        .
                '''

                echo 'Filesystem vulnerability scan passed.'


                // -------------------------------------------------
                // 2. BUILD DOCKER IMAGE
                // -------------------------------------------------

                echo 'Building Docker image...'

                sh '''
                    docker build \
                        --no-cache \
                        -t "$IMAGE" \
                        .
                '''

                echo "Docker image built successfully: $IMAGE"


                // -------------------------------------------------
                // 3. DOCKER IMAGE / LAYER SCAN
                // -------------------------------------------------

                echo 'Scanning Docker image with Trivy...'

                sh '''
                    trivy image \
                        --scanners vuln \
                        --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
                        --exit-code 1 \
                        "$IMAGE"
                '''

                echo 'Docker image vulnerability scan passed.'

                echo '=========================================='
                echo 'VULNERABILITY SCAN PASSED'
                echo '=========================================='
            }
        }


        // =====================================================
        // STAGE D - PUSH TO LOCAL REGISTRY
        // =====================================================

        stage('D - Push to Local Registry') {
            steps {

                echo '=========================================='
                echo 'Stage D - Push Docker Image'
                echo '=========================================='

                echo "Image: ${IMAGE}"

                sh '''
                    docker push "$IMAGE"
                '''

                echo '=========================================='
                echo 'DOCKER IMAGE PUSHED SUCCESSFULLY'
                echo '=========================================='
            }
        }
    }


    // =========================================================
    // POST BUILD
    // =========================================================

    post {

        success {

            echo '=========================================='
            echo 'PIPELINE SUCCESSFUL'
            echo '=========================================='

            echo "Docker Image: ${IMAGE}"

            echo 'All stages completed successfully.'
        }

        failure {

            echo '=========================================='
            echo 'PIPELINE FAILED'
            echo '=========================================='

            echo 'One or more stages failed.'

            echo 'If Stage C failed, the Docker image was NOT pushed.'
        }

        always {

            echo '=========================================='
            echo 'PIPELINE COMPLETED'
            echo '=========================================='
        }
    }
}