pipeline {
    agent any

    stages {

        stage('PR Validation') {
            when {
                changeRequest()   // Runs only for PR
            }
            stages {
                stage('Notification') {
                    steps { echo "Stage 1: Notification" }
                }
                stage('Checkout') {
                    steps { echo "Stage 2: Checkout" }
                }
                stage('SonarQube') {
                    steps { echo "Stage 3: Sonar" }
                }
                stage('Docker Build') {
                    steps { echo "Stage 4: Build" }
                }
                stage('Push Image') {
                    steps { echo "Stage 5: Push" }
                }
            }
        }

        stage('Deployment') {
            when {
                branch 'develop'   // Runs only after merge
            }
            steps {
                echo "Stage 6: Deploy"
            }
        }
    }
}
