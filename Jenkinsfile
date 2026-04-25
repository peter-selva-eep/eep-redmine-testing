pipeline {
    agent any 
 
    /*
    ─────────────────────────────────────────────────────────────
     BRANCH STRATEGY
       • PR opened / new commit pushed  → Stages 1-5  (CI only)
       • PR merged into develop         → Stages 1-6  (CI + Deploy)

     Jenkins multibranch pipeline exposes:
       env.BRANCH_NAME          → e.g. "PR-42"  or  "develop"
       env.CHANGE_ID            → set ONLY on PR builds
       env.CHANGE_TARGET        → target branch of the PR  (e.g. "develop")
    ─────────────────────────────────────────────────────────────
    */

    environment {
        // ── Project settings ───────────────────────────────────
        APP_NAME        = 'your-app-name'
        ECR_REGISTRY    = '123456789012.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPO        = 'your-ecr-repo-name'
        K8S_DEPLOYMENT  = 'your-k8s-deployment-name'
        K8S_CONTAINER   = 'your-container-name'
        GOOGLE_CHAT_SPACE = 'your-google-chat-webhook-url'

        // ── Derived ────────────────────────────────────────────
        IMAGE_TAG       = "${env.BUILD_NUMBER}"
        IS_PR_BUILD     = "${env.CHANGE_ID != null}"          // true  → PR build
        IS_MERGE_BUILD  = "${env.BRANCH_NAME == 'develop' && env.CHANGE_ID == null}" // true → merged
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    stages {

        // ── Stage 1: Notification ──────────────────────────────
        stage('Deployment Started Notification') {
            steps {
                script {
                    def triggerType = env.CHANGE_ID
                        ? "PR-${env.CHANGE_ID} | ${env.CHANGE_BRANCH} → ${env.CHANGE_TARGET}"
                        : "Merge to ${env.BRANCH_NAME}"

                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo " [STAGE 1] Deployment Started Notification"
                    echo " Trigger  : ${triggerType}"
                    echo " Build No : ${env.BUILD_NUMBER}"
                    echo " Job Name : ${env.JOB_NAME}"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

                    // TODO: Replace echo with real Google Chat webhook call
                    // example:
                    // httpRequest(
                    //     url: "${GOOGLE_CHAT_SPACE}",
                    //     httpMode: 'POST',
                    //     contentType: 'APPLICATION_JSON',
                    //     requestBody: """{"text": "🚀 Pipeline started for ${triggerType}"}"""
                    // )
                }
            }
        }

        // ── Stage 2: Git Checkout ──────────────────────────────
        stage('Git Checkout') {
            steps {
                script {
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo " [STAGE 2] Git Checkout"
                    echo " Branch   : ${env.BRANCH_NAME}"
                    echo " Commit   : ${env.GIT_COMMIT ?: 'N/A'}"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

                    // TODO: Replace with actual checkout when using scripted SCM
                    // checkout scm    ← (already done automatically in Multibranch Pipeline)
                }
            }
        }

        // ── Stage 3: SonarQube Scan ────────────────────────────
        stage('SonarQube Scan') {
            steps {
                script {
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo " [STAGE 3] SonarQube Scan"
                    echo " Scanning project: ${APP_NAME}"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

                    // TODO: Replace with real SonarQube scan
                    // withSonarQubeEnv('SonarQube') {
                    //     sh 'mvn sonar:sonar'   // or your build tool
                    // }
                    // waitForQualityGate abortPipeline: true
                }
            }
        }

        // ── Stage 4: Docker Build ──────────────────────────────
        stage('Docker Build') {
            steps {
                script {
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo " [STAGE 4] Docker Build"
                    echo " Image    : ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

                    // TODO: Replace with real Docker build
                    // sh "docker build -t ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG} ."
                }
            }
        }

        // ── Stage 5: Docker Image Push to ECR ─────────────────
        stage('Docker Image Push To ECR') {
            steps {
                script {
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo " [STAGE 5] Docker Image Push To ECR"
                    echo " Pushing  : ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

                    // TODO: Replace with real ECR push
                    // sh """
                    //     aws ecr get-login-password --region ap-south-1 \
                    //         | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                    //     docker push ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
                    // """
                }
            }
        }

        // ── Stage 6: Kubectl Set Image  (MERGE ONLY) ──────────
        stage('Kubectl Set Image') {
            /*
              This stage runs ONLY when the build is triggered by a
              merge into develop (not on PR/feature branch builds).
              CHANGE_ID is null  →  this is a direct branch build (post-merge)
              BRANCH_NAME == 'develop'  →  confirms target branch
            */
            when {
                allOf {
                    branch 'develop'
                    not { changeRequest() }   // changeRequest() is true only on PR builds
                }
            }
            steps {
                script {
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo " [STAGE 6] Kubectl Set Image"
                    echo " Deployment : ${K8S_DEPLOYMENT}"
                    echo " Container  : ${K8S_CONTAINER}"
                    echo " New Image  : ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}"
                    echo " ✅ Running because PR was MERGED into develop"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

                    // TODO: Replace with real kubectl command
                    // sh """
                    //     kubectl set image deployment/${K8S_DEPLOYMENT} \
                    //         ${K8S_CONTAINER}=${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG} \
                    //         --record
                    // """
                }
            }
        }

    } // end stages

    // ── Post Actions ───────────────────────────────────────────
    post {
        success {
            script {
                def msg = env.CHANGE_ID
                    ? "✅ PR-${env.CHANGE_ID} CI passed (Stages 1-5). Ready for Architect review & merge."
                    : "✅ Deploy complete (Stages 1-6). develop branch is live."

                echo "[POST] SUCCESS → ${msg}"
                // TODO: Send to Google Chat space
            }
        }
        failure {
            script {
                def msg = env.CHANGE_ID
                    ? "❌ PR-${env.CHANGE_ID} CI FAILED. Please fix before requesting review."
                    : "❌ Deploy FAILED on develop. Investigate immediately."

                echo "[POST] FAILURE → ${msg}"
                // TODO: Send alert to Google Chat space
            }
        }
        always {
            echo "[POST] Pipeline finished — Build #${env.BUILD_NUMBER}"
        }
    }

}
