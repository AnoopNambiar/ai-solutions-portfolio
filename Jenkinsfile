pipeline {

    agent any

    environment {
        APP_NAME   = "nasa-app"
        REGISTRY   = "localhost:5000"
        IMAGE      = "nasa-app:1.0"
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
                    echo "Flake8:"
                    python -m flake8 --version

                    echo ""
                    echo "Pytest:"
                    python -m pytest --version

                    echo ""
                    echo "Black:"
                    python -m black --version

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
        // STAGE A - CODE LINTING
        // =====================================================

        stage('A - Code Linting') {
            steps {
                echo '=========================================='
                echo 'Stage A - Code Linting'
                echo '=========================================='

                echo 'Running Flake8...'

                sh '''
                    python -m flake8 *.py tests
                '''

                echo 'Running Black format check...'

                sh '''
                    python -m black --check *.py tests
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

                sh '''
                    python -m pytest -v
                '''

                echo 'Unit tests completed successfully.'
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
                // Scan source files and dependencies
                // -------------------------------------------------

                echo 'Scanning project dependencies with Trivy...'

                sh '''
                    trivy fs \
                        --scanners vuln \
                        --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
                        --exit-code 1 \
                        .
                '''


                // -------------------------------------------------
                // Build Docker image
                // -------------------------------------------------

                echo 'Building Docker image...'

                sh '''
                    docker build \
                        -t "$IMAGE" \
                        .
                '''


                // -------------------------------------------------
                // Scan Docker image and its layers
                // -------------------------------------------------

                echo 'Scanning Docker image with Trivy...'

                sh '''
                    trivy image \
                        --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
                        --exit-code 1 \
                        "$IMAGE"
                '''

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