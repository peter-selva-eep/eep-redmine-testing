pipeline {
    agent any

    stages {

        // 🔹 PR Validation Pipeline
        stage('PR Validation') {
            when {
                changeRequest()
            }
            stages {
                stage('Notification') {
                    steps { echo "PR: Notification" }
                }
                stage('Checkout') {
                    steps { echo "PR: Checkout" }
                }
                stage('SonarQube') {
                    steps { echo "PR: Sonar" }
                }
                stage('Docker Build') {
                    steps { echo "PR: Build Docker Image (no push)" }
                }
            }
        }

        // 🔹 Post-Merge Pipeline (Develop Branch)
        stage('Build & Push') {
            when {
                branch 'develop'
            }
            stages {
                stage('Checkout') {
                    steps { echo "Merge: Checkout" }
                }
                stage('Docker Build') {
                    steps { echo "Merge: Build Docker Image" }
                }
                stage('Push to ECR') {
                    steps { echo "Merge: Push to ECR" }
                }
            }
        }

        stage('Deployment') {
            when {
                branch 'develop'
            }
            steps {
                echo "Merge: Deploy using kubectl"
            }
        }
    }
}
