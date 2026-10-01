pipeline {

    agent any

    environment {
        APP_NAME   = "nasa-app"
        REGISTRY   = "localhost:5000"
        IMAGE      = "nasa-app:1.0"
    }

    stages {

        // =========================================================
        // ENVIRONMENT CHECK
        // =========================================================

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


        // =========================================================
        // STAGE A - CODE LINTING
        // =========================================================

        stage('A - Code Linting') {
            steps {

                echo '=========================================='
                echo 'Stage A - Code Linting'
                echo '=========================================='

                echo 'Running Flake8...'

                sh '''
                    python -m flake8 *.py tests
                '''

                echo 'Checking Black formatting...'

                sh '''
                    python -m black --check *.py tests
                '''
            }
        }


        // =========================================================
        // STAGE B - UNIT TESTING
        // =========================================================

        stage('B - Unit Testing') {
            steps {

                echo '=========================================='
                echo 'Stage B - Unit Testing'
                echo '=========================================='

                sh '''
                    python -m pytest -v
                '''
            }
        }


        // =========================================================
        // STAGE C - VULNERABILITY SCAN
        // =========================================================

        stage('C - Vulnerability Scan') {
            steps {

                echo '=========================================='
                echo 'Stage C - Vulnerability Scan'
                echo '=========================================='

                // ---------------------------------------------
                // Scan application dependencies / filesystem
                // ---------------------------------------------

                echo 'Scanning project dependencies with Trivy...'

                sh '''
                    trivy fs \
                        --scanners vuln \
                        --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL \
                        --exit-code 1 \
                        .
                '''


                // ---------------------------------------------
                // Build Docker image
                // ---------------------------------------------

                echo 'Building Docker image...'

                sh '''
                    docker build \
                        -t "$IMAGE" \
                        .
                '''


                // ---------------------------------------------
                // Scan Docker image
                // ---------------------------------------------

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


        // =========================================================
        // STAGE D - PUSH TO LOCAL REGISTRY
        // =========================================================

        stage('D - Push to Local Registry') {
            steps {

                echo '=========================================='
                echo 'Stage D - Push Docker Image'
                echo '=========================================='

                echo "Pushing image: ${IMAGE}"

                sh '''
                    docker push "$IMAGE"
                '''

                echo '=========================================='
                echo 'Docker image pushed successfully'
                echo '=========================================='
            }
        }
    }


    // =============================================================
    // POST BUILD
    // =============================================================

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

            echo 'If the vulnerability scan failed,'
            echo 'the Docker image was NOT pushed to the registry.'
        }

        always {

            echo '=========================================='
            echo 'Pipeline completed'
            echo '=========================================='
        }
    }
}