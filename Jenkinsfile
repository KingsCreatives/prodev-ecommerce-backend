pipeline {
    agent any

    environment {
        DOCKER_CREDS = credentials('docker-hub-credentials')
        IMAGE_NAME = "kwamecody172/prodev-backend"
        TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh 'echo "Setting up environment..."'
                sh 'touch infra/docker/.env'
            }
        }

        stage('Test') {
            steps {
                script {
                    try {
                        sh 'docker compose -f infra/docker/docker-compose.yml up -d db redis'
                        sh 'sleep 10' 
                        sh 'docker compose -f infra/docker/docker-compose.yml run web python src/manage.py test src'
                    } finally {
                        sh 'docker compose -f infra/docker/docker-compose.yml down -v'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${TAG} -t ${IMAGE_NAME}:latest -f infra/docker/Dockerfile ."
                }
            }
        }

        stage('Push to Docker Hub') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh "echo ${DOCKER_CREDS_PSW} | docker login -u ${DOCKER_CREDS_USR} --password-stdin"
                    sh "docker push ${IMAGE_NAME}:${TAG}"
                    sh "docker push ${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Deploy to K8s') {
             when {
                branch 'main'
            }
            steps {
                sh "kubectl set image deployment/web web=${IMAGE_NAME}:${TAG}"
                sh "kubectl set image deployment/celery-worker worker=${IMAGE_NAME}:${TAG}"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}