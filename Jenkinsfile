pipeline {
    agent any

    stages {

        stage('Step 1: Deployment Start Notification') {
            steps { 
                echo "Step 1: Deployment Start Notification - Started"
            }
        }

        stage('Step 2: Git Checkout') {
            steps {
                echo "Step 2: Git Checkout - Checking out branch features/152"
            }
        }

        stage('Step 3: SonarQube Scanner') {
            when {
                anyOf {
                    changeRequest()
                    branch 'features/*'
                }
            }
            steps {
                echo "Step 3: SonarQube Scanner - Running code quality scan"
            }
        }

        stage('Step 4: Docker Build') {
            when {
                anyOf {
                    changeRequest()
                    branch 'features/*'
                }
            }
            steps {
                echo "Step 4: Docker Build - Building Docker image"
            }
        }

        stage('Step 5: Docker Image Push to ECR') {
            when {
                anyOf {
                    changeRequest()
                    branch 'features/*'
                }
            }
            steps {
                echo "Step 5: Docker Image Push to ECR - Pushing image to registry"
            }
        }

        stage('Approve and Merge PR') {
            when {
                changeRequest target: 'develop'
            }
            steps {
                echo "Step 1 to 5 completed successfully - Waiting for manual approval to merge PR features/152 into develop"
                input message: 'All steps passed. Do you want to approve and merge this PR into develop?',
                      ok: 'Approve & Merge'
                echo "PR manually approved - Merging features/152 into develop"
            }
        }

        stage('Step 6: Kubectl Set Image') {
            when {
                allOf {
                    branch 'develop'
                    not { changeRequest() }
                }
            }
            steps {
                echo "Step 6: Kubectl Set Image - Updating Kubernetes deployment with new image"
            }
        }

        stage('Step 7: Deployment Completed Notification') {
            when {
                allOf {
                    branch 'develop'
                    not { changeRequest() }
                }
            }
            steps {
                echo "Step 7: Deployment Completed Notification - Deployment finished successfully"
            }
        }

    }

    post {
        failure {
            echo "Pipeline FAILED - Sending failure notification"
        }
        success {
            echo "Pipeline SUCCEEDED"
        }
    }
}
