pipeline {
    agent any

    stages {

        // 🔹 PR Validation Pipeline
        stage('PR Pipeline') {
            when {
                changeRequest()
            }
            stages {

                stage('Checkout') {
                    steps { echo "PR: Checkout code" }
                }

                stage('Deployment Start Notification') {
                    steps { echo "PR: Deployment started notification" }
                }

                stage('SonarQube Scan') {
                    steps { echo "PR: Running SonarQube scan" }
                }

                stage('Docker Build') {
                    steps { echo "PR: Build Docker Image (no push)" }
                }
            }
        }

        // 🔹 Post-Merge Pipeline (Develop Branch)
        stage('Post Merge Pipeline') {
            when {
                branch 'develop'
            }
            stages {

                stage('Docker Build') {
                    steps { echo "Merge: Build Docker Image" }
                }

                stage('Push to ECR') {
                    steps { echo "Merge: Push Docker Image to ECR" }
                }

                stage('Deploy to Kubernetes') {
                    steps { echo "Merge: Deploy to Kubernetes" }
                }
            }
        }
    }
}
