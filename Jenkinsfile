pipeline {
    agent any

    parameters {
        string(name: 'TRIGGER', defaultValue: 'ci', description: 'ci = before merge, cd = after merge')
        string(name: 'SHA', defaultValue: '', description: 'Git commit SHA')
        string(name: 'BRANCH', defaultValue: '', description: 'Branch name')
        string(name: 'PR_NUMBER', defaultValue: '', description: 'PR number')
    }

    environment {
        GITHUB_TOKEN = credentials('github-token')
        GITHUB_REPO  = "eva-equity-partners-testing-01/eep-redmine-testing-main"
    }

    stages {

        stage('Step 1 - Checkout') {
            when { expression { params.TRIGGER == 'ci' } }
            steps {
                echo "🔃 Step 1: Git Checkout Started..."
                echo "✅ Step 1: Git Checkout Completed"
            }
        }

        stage('Step 2 - Notification') {
            when { expression { params.TRIGGER == 'ci' } }
            steps {
                echo "🔔 Step 2: Deployment Notification Sent"
            }
        }

        stage('Step 3 - SonarQube') {
            when { expression { params.TRIGGER == 'ci' } }
            steps {
                echo "🔍 Step 3: SonarQube Validation Started..."
                echo "✅ Step 3: SonarQube Validation Completed"
            }
        }

        stage('Step 4 - Docker Build') {
<<<<<<< Updated upstream
            // Runs only on features/* branch
            when {
                branch 'features/*'
            }
=======
            when { expression { params.TRIGGER == 'ci' } }
>>>>>>> Stashed changes
            steps {
                echo "🐳 Step 4: Docker Build Started..."
                echo "✅ Step 4: Docker Build Completed"
            }
        }

<<<<<<< Updated upstream
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
=======
        stage('Step 5 - Deploy to QA') {
            when { expression { params.TRIGGER == 'cd' } }
            steps {
                echo "🚀 Step 5: Deploying to QA environment..."
                echo "✅ Step 5: Deployment to QA Completed!"
>>>>>>> Stashed changes
            }
        }

    }

    post {
        success {
            script {
                if (params.TRIGGER == 'ci') {
                    echo "✅ CI Build #${BUILD_NUMBER} SUCCESS — Ready to merge!"
                    if (params.SHA) {
                        sh """
                            curl -s -X POST \\
                            -H "Authorization: token ${GITHUB_TOKEN}" \\
                            -H "Content-Type: application/json" \\
                            -d '{"state":"success","context":"continuous-integration/jenkins","description":"CI passed! Ready to merge.","target_url":"${BUILD_URL}"}' \\
                            https://api.github.com/repos/${GITHUB_REPO}/statuses/${params.SHA}
                        """
                    }
                } else {
                    echo "✅ CD Build #${BUILD_NUMBER} SUCCESS — Deployed to QA!"
                }
            }
        }
        failure {
            script {
                if (params.TRIGGER == 'ci') {
                    echo "❌ CI Build #${BUILD_NUMBER} FAILED"
                    if (params.SHA) {
                        sh """
                            curl -s -X POST \\
                            -H "Authorization: token ${GITHUB_TOKEN}" \\
                            -H "Content-Type: application/json" \\
                            -d '{"state":"failure","context":"continuous-integration/jenkins","description":"CI failed! Fix before merging.","target_url":"${BUILD_URL}"}' \\
                            https://api.github.com/repos/${GITHUB_REPO}/statuses/${params.SHA}
                        """
                    }
                } else {
                    echo "❌ CD Build #${BUILD_NUMBER} FAILED"
                }
            }
        }
    }
}
