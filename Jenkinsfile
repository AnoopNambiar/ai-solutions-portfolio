pipeline {

    agent any

    environment {
        APP_NAME       = "nasa-app"
        REGISTRY       = "localhost:5000"
        IMAGE          = "nasa-app:1.0"
        REGISTRY_IMAGE = "localhost:5000/nasa-app:1.0"

        PYTHON         = ".venv/Scripts/python.exe"
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
                    if [ ! -d ".venv" ]; then
                        echo "Creating Python virtual environment..."
                        python -m venv .venv
                    else
                        echo "Python virtual environment already exists."
                    fi

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

                echo 'Running Flake8...'

                sh '''
                    .venv/Scripts/python.exe -m flake8 *.py tests
                '''

                echo 'Flake8 passed.'

                echo 'Running Black format check...'

                sh '''
                    .venv/Scripts/python.exe -m black --check *.py tests
                '''

                echo 'Black passed.'
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
                    echo "=== Docker Version ==="
                    docker --version

                    echo "=== Docker Context ==="
                    docker context show

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
                // 1. PYTHON DEPENDENCY SCAN
                // -------------------------------------------------
                //
                // Scan requirements.txt directly rather than the
                // complete workspace. This prevents .venv and pip's
                // embedded bom.cdx.json from being treated as the
                // application's dependency inventory.
                //

                echo 'Scanning Python dependencies with Trivy...'

                sh '''
                    trivy fs \
                        --scanners vuln \
                        --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
                        --ignore-unfixed \
                        --exit-code 1 \
                        requirements.txt
                '''

                echo 'Python dependency vulnerability scan passed.'


                // -------------------------------------------------
                // 2. BUILD DOCKER IMAGE
                // -------------------------------------------------

                echo 'Building Docker image...'

                sh '''
                    docker build \
                        --pull \
                        --no-cache \
                        -t "$IMAGE" \
                        .
                '''

                echo "Docker image built successfully: $IMAGE"


                // -------------------------------------------------
                // 3. DOCKER OS / CONTAINER LAYER SCAN
                // -------------------------------------------------
                //
                // Python dependencies are already scanned above.
                // Therefore the image scan is restricted to OS
                // packages to avoid pip's embedded BOM false positives.
                //

                echo 'Scanning Docker image OS packages with Trivy...'

                sh '''
                    trivy image \
                        --scanners vuln \
                        --pkg-types os \
                        --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
                        --ignore-unfixed \
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

                echo "Source Image: ${IMAGE}"
                echo "Registry Image: ${REGISTRY_IMAGE}"

                sh '''
                    echo "Tagging image for local registry..."

                    docker tag \
                        "$IMAGE" \
                        "$REGISTRY_IMAGE"

                    echo "Pushing image to local registry..."

                    docker push "$REGISTRY_IMAGE"
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
            echo "Registry Image: ${REGISTRY_IMAGE}"

            echo 'All stages completed successfully.'
        }

        failure {

            echo '=========================================='
            echo 'PIPELINE FAILED'
            echo '=========================================='

            echo 'One or more stages failed.'
            echo 'Stage D is executed only when all previous stages pass.'
            echo 'If Stage C failed, the Docker image was NOT pushed.'
        }

        always {

            echo '=========================================='
            echo 'PIPELINE COMPLETED'
            echo '=========================================='
        }
    }
}