pipeline {
    agent any

    environment {
        APP_NAME            = 'your-app-name'
        ECR_REGISTRY        = '123456789012.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPO            = 'your-ecr-repo-name'
        AWS_REGION          = 'ap-south-1'
        K8S_DEPLOYMENT      = 'your-k8s-deployment-name'
        K8S_CONTAINER       = 'your-container-name'
        K8S_NAMESPACE       = 'default'
        SONARQUBE_SERVER    = 'SonarQube'
        GOOGLE_CHAT_WEBHOOK = 'your-google-chat-webhook-url'
        IMAGE_TAG           = "${env.BUILD_NUMBER}"
        IMAGE_FULL          = "${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {

        stage('Deployment Started Notification') {
            when {
                anyOf {
                    allOf {
                        branch 'develop'
                        not { changeRequest() }
                    }
                    allOf {
                        changeRequest target: 'develop'
                        anyOf {
                            changeRequest branch: 'features/*'
                            changeRequest branch: 'bugs/*'
                            changeRequest branch: 'release/*'
                            changeRequest branch: 'hotfix/*'
                        }
                    }
                }
            }
            steps {
                echo "Stage 1 : Deployment Started Notification"
            }
        }

        stage('Git Checkout') {
            when {
                anyOf {
                    allOf {
                        branch 'develop'
                        not { changeRequest() }
                    }
                    allOf {
                        changeRequest target: 'develop'
                        anyOf {
                            changeRequest branch: 'features/*'
                            changeRequest branch: 'bugs/*'
                            changeRequest branch: 'release/*'
                            changeRequest branch: 'hotfix/*'
                        }
                    }
                }
            }
            steps {
                echo "Stage 2 : Git Checkout"
            }
        }

        stage('SonarQube Scan') {
            when {
                anyOf {
                    allOf {
                        branch 'develop'
                        not { changeRequest() }
                    }
                    allOf {
                        changeRequest target: 'develop'
                        anyOf {
                            changeRequest branch: 'features/*'
                            changeRequest branch: 'bugs/*'
                            changeRequest branch: 'release/*'
                            changeRequest branch: 'hotfix/*'
                        }
                    }
                }
            }
            steps {
                echo "Stage 3 : SonarQube Scan"
            }
        }

        stage('Docker Build') {
            when {
                anyOf {
                    allOf {
                        branch 'develop'
                        not { changeRequest() }
                    }
                    allOf {
                        changeRequest target: 'develop'
                        anyOf {
                            changeRequest branch: 'features/*'
                            changeRequest branch: 'bugs/*'
                            changeRequest branch: 'release/*'
                            changeRequest branch: 'hotfix/*'
                        }
                    }
                }
            }
            steps {
                echo "Stage 4 : Docker Build"
            }
        }

        stage('Docker Image Push To ECR') {
            when {
                anyOf {
                    allOf {
                        branch 'develop'
                        not { changeRequest() }
                    }
                    allOf {
                        changeRequest target: 'develop'
                        anyOf {
                            changeRequest branch: 'features/*'
                            changeRequest branch: 'bugs/*'
                            changeRequest branch: 'release/*'
                            changeRequest branch: 'hotfix/*'
                        }
                    }
                }
            }
            steps {
                echo "Stage 5 : Docker Image Push To ECR"
            }
        }

        stage('Kubectl Set Image') {
            when {
                allOf {
                    branch 'develop'
                    not { changeRequest() }
                }
            }
            steps {
                echo "Stage 6 : Kubectl Set Image - Merge build only"
            }
        }

    }

    post {
        success {
            echo "Pipeline SUCCESS - Build #${env.BUILD_NUMBER}"
        }
        failure {
            echo "Pipeline FAILED - Build #${env.BUILD_NUMBER}"
        }
        always {
            echo "Pipeline finished - ${currentBuild.currentResult}"
        }
    }

}
