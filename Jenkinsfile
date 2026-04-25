pipeline {
    agent any

    /*
    ══════════════════════════════════════════════════════════════════
     BEST PRACTICE — BUILD ONCE, PROMOTE ON MERGE
    ──────────────────────────────────────────────────────────────────
     PR BUILD   (features|bugs|release|hotfix → develop)
       Stage 1  Notification
       Stage 2  Git Checkout
       Stage 3  SonarQube Scan
       Stage 4  Docker Build
       Stage 5  Push to ECR  →  tagged as  pr-<PR_ID>-<BUILD_NO>

     MERGE BUILD (PR merged into develop)
       Stage 1  Notification
       Stage 6  Retag PR image → develop-latest  +  kubectl deploy

     WHY THIS IS BETTER
       - Docker image is built ONCE on the PR
       - The EXACT same image that passed CI gets deployed
       - No wasted rebuild on merge
       - You can always trace which PR image is running in K8s
    ══════════════════════════════════════════════════════════════════
    */

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

        // PR build  → image tagged as  pr-42-build-7
        // Merge build → retagged as    develop-latest
        PR_IMAGE_TAG        = "pr-${env.CHANGE_ID ?: 'merge'}-build-${env.BUILD_NUMBER}"
        DEPLOY_IMAGE_TAG    = "develop-latest"

        PR_IMAGE_FULL       = "${ECR_REGISTRY}/${ECR_REPO}:${PR_IMAGE_TAG}"
        DEPLOY_IMAGE_FULL   = "${ECR_REGISTRY}/${ECR_REPO}:${DEPLOY_IMAGE_TAG}"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {

        // ══════════════════════════════════════════════════════════
        //  STAGE 1 — Notification
        //  Runs on: BOTH PR build and Merge build
        // ══════════════════════════════════════════════════════════
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

        // ══════════════════════════════════════════════════════════
        //  STAGE 2 — Git Checkout
        //  Runs on: PR build only
        // ══════════════════════════════════════════════════════════
        stage('Git Checkout') {
            when {
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
            steps {
                echo "Stage 2 : Git Checkout"
                // checkout scm
            }
        }

        // ══════════════════════════════════════════════════════════
        //  STAGE 3 — SonarQube Scan
        //  Runs on: PR build only
        // ══════════════════════════════════════════════════════════
        stage('SonarQube Scan') {
            when {
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
            steps {
                echo "Stage 3 : SonarQube Scan"
                // withSonarQubeEnv("${SONARQUBE_SERVER}") { sh 'mvn sonar:sonar' }
                // waitForQualityGate abortPipeline: true
            }
        }

        // ══════════════════════════════════════════════════════════
        //  STAGE 4 — Docker Build
        //  Runs on: PR build only
        //  Tags image as  pr-<PR_ID>-build-<BUILD_NO>
        // ══════════════════════════════════════════════════════════
        stage('Docker Build') {
            when {
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
            steps {
                echo "Stage 4 : Docker Build → ${PR_IMAGE_FULL}"
                // sh "docker build -t ${PR_IMAGE_FULL} ."
            }
        }

        // ══════════════════════════════════════════════════════════
        //  STAGE 5 — Docker Image Push To ECR
        //  Runs on: PR build only
        //  Pushes  pr-<PR_ID>-build-<BUILD_NO>  to ECR
        // ══════════════════════════════════════════════════════════
        stage('Docker Image Push To ECR') {
            when {
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
            steps {
                echo "Stage 5 : Docker Image Push To ECR → ${PR_IMAGE_FULL}"
                // sh """
                //     aws ecr get-login-password --region ${AWS_REGION} \
                //         | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                //     docker push ${PR_IMAGE_FULL}
                // """
            }
        }

        // ══════════════════════════════════════════════════════════
        //  STAGE 6 — Retag + Kubectl Deploy
        //  Runs on: MERGE build only
        //
        //  Takes the PR image already in ECR
        //  Retags it as develop-latest
        //  Deploys that image to Kubernetes
        //
        //  NO REBUILD — same image that passed CI gets deployed
        // ══════════════════════════════════════════════════════════
        stage('Kubectl Set Image') {
            when {
                allOf {
                    branch 'develop'
                    not { changeRequest() }
                }
            }
            steps {
                echo "Stage 6 : Retag PR image → ${DEPLOY_IMAGE_FULL} and deploy to K8s"
                // sh """
                //     // Pull the PR image from ECR
                //     aws ecr get-login-password --region ${AWS_REGION} \
                //         | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                //
                //     // Retag as develop-latest
                //     docker pull ${PR_IMAGE_FULL}
                //     docker tag  ${PR_IMAGE_FULL} ${DEPLOY_IMAGE_FULL}
                //     docker push ${DEPLOY_IMAGE_FULL}
                //
                //     // Deploy to Kubernetes
                //     kubectl set image deployment/${K8S_DEPLOYMENT} \
                //         ${K8S_CONTAINER}=${DEPLOY_IMAGE_FULL} \
                //         --namespace=${K8S_NAMESPACE} \
                //         --record
                //     kubectl rollout status deployment/${K8S_DEPLOYMENT} \
                //         --namespace=${K8S_NAMESPACE}
                // """
            }
        }

    } // end stages

    post {
        success {
            script {
                def msg = env.CHANGE_ID
                    ? "Stage 1-5 passed for PR-${env.CHANGE_ID} — ready for architect review"
                    : "Merge build complete — develop deployed to Kubernetes"
                echo "[POST] SUCCESS → ${msg}"
            }
        }
        failure {
            script {
                def msg = env.CHANGE_ID
                    ? "Pipeline FAILED for PR-${env.CHANGE_ID} — fix before review"
                    : "Merge build FAILED on develop — investigate immediately"
                echo "[POST] FAILURE → ${msg}"
            }
        }
        always {
            echo "[POST] Build #${env.BUILD_NUMBER} → ${currentBuild.currentResult}"
        }
    }

}
