pipeline {
    agent any

    environment {
        IMAGE_NAME = "fastapi-demo"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

    }

    post {
        success {
            echo "✅ Build #${BUILD_NUMBER} SUCCESS — image ${IMAGE_NAME}:${IMAGE_TAG} ready"
            sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"
        }
        failure {
            echo "❌ Build #${BUILD_NUMBER} FAILED"
        }
    }
}
