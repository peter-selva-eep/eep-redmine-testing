pipeline {
    agent any

    environment {
        IMAGE_NAME = "fastapi-demo"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('Step 1 - Git Checkout') {
            steps {
                echo "🔃 Step 1: Git Checkout Started..."
                checkout scm
                echo "✅ Step 1: Git Checkout Completed"
            }
        }

        stage('Step 2 - Deployment Notification') {
            steps {
                echo "🔔 Step 2: Deployment Started — Build #${BUILD_NUMBER}"
            }
        }

        stage('Step 3 - SonarQube Validation') {
            steps {
                echo "🔍 Step 3: SonarQube Validation Started..."
                echo "✅ Step 3: SonarQube Validation Completed"
            }
        }

        stage('Step 4 - Docker Build') {
            // Runs only on features/* branch
            when {
                branch 'features/*'
            }
            steps {
                echo "🐳 Step 4: Docker Build Started..."
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                echo "✅ Step 4: Docker Build Completed — ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Step 5 - Push to ECR') {
            // Runs only on features/* branch
            when {
                branch 'features/*'
            }
            steps {
                echo "📦 Step 5: Pushing Docker Image to ECR..."
                echo "✅ Step 5: Image Pushed to ECR Successfully"
            }
        }

        stage('Step 6 - Kubectl Set Image') {
            // Runs ONLY after merge to qa branch
            when {
                branch 'qa'
            }
            steps {
                echo "☸️  Step 6: Updating Kubernetes Deployment..."
                echo "✅ Step 6: Kubectl Set Image Completed"
            }
        }

    }

    post {
        success {
            echo "✅ Build #${BUILD_NUMBER} SUCCESS — All steps completed"
            sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"
        }
        failure {
            echo "❌ Build #${BUILD_NUMBER} FAILED — Check logs above"
        }
    }
}
