pipeline {
    agent any

    environment {
        AWS_HOST = '여기에_AWS_PUBLIC_IP'
        AWS_USER = 'ubuntu'

        PROJECT_DIR = '/home/ubuntu/project'
        IMAGE_DIR = '/home/ubuntu/image-rag-data/images'

        GITHUB_REPO = 'https://github.com/여기에아이디/여기에저장소.git'
        GITHUB_BRANCH = 'main'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Project') {
            steps {
                sh '''
                    echo "================================"
                    echo "Project files"
                    echo "================================"

                    ls -la

                    echo "================================"
                    echo "Backend"
                    echo "================================"

                    ls -la backend

                    echo "================================"
                    echo "Frontend"
                    echo "================================"

                    ls -la frontend
                '''
            }
        }

        stage('Build Test') {
            steps {
                sh '''
                    docker compose config
                    docker compose build
                '''
            }
        }

        stage('Deploy AWS') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'openai-api-key',
                        variable: 'OPENAI_API_KEY'
                    )
                ]) {

                    sshagent(
                        credentials: ['aws-ec2-ssh']
                    ) {

                        sh '''
                            ssh -o StrictHostKeyChecking=no \
                            ${AWS_USER}@${AWS_HOST} \
                            "
                                if [ ! -d '${PROJECT_DIR}/.git' ]; then
                                    git clone \
                                    -b ${GITHUB_BRANCH} \
                                    ${GITHUB_REPO} \
                                    ${PROJECT_DIR}
                                fi
                            "
                        '''

                        sh '''
                            ssh -o StrictHostKeyChecking=no \
                            ${AWS_USER}@${AWS_HOST} \
                            "
                                cd ${PROJECT_DIR}

                                git fetch origin

                                git reset --hard \
                                origin/${GITHUB_BRANCH}

                                mkdir -p \
                                ${IMAGE_DIR}
                            "
                        '''

                        sh '''
                            printf '%s\n' \
                            "OPENAI_API_KEY=${OPENAI_API_KEY}" \
                            > backend.env
                        '''

                        sh '''
                            printf '%s\n' \
                            "IMAGE_HOST_PATH=${IMAGE_DIR}" \
                            > root.env
                        '''

                        sh '''
                            scp \
                            -o StrictHostKeyChecking=no \
                            backend.env \
                            ${AWS_USER}@${AWS_HOST}:${PROJECT_DIR}/backend/.env
                        '''

                        sh '''
                            scp \
                            -o StrictHostKeyChecking=no \
                            root.env \
                            ${AWS_USER}@${AWS_HOST}:${PROJECT_DIR}/.env
                        '''

                        sh '''
                            rm -f \
                            backend.env \
                            root.env
                        '''

                        sh '''
                            ssh -o StrictHostKeyChecking=no \
                            ${AWS_USER}@${AWS_HOST} \
                            "
                                cd ${PROJECT_DIR}

                                docker compose down

                                docker compose up \
                                -d \
                                --build

                                docker image prune \
                                -f
                            "
                        '''
                    }
                }
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 5

                    curl \
                    --fail \
                    --retry 5 \
                    --retry-delay 3 \
                    http://${AWS_HOST}/
                '''
            }
        }
    }

    post {
        success {
            echo '================================'
            echo 'AWS DEPLOY SUCCESS'
            echo '================================'
        }

        failure {
            echo '================================'
            echo 'AWS DEPLOY FAILED'
            echo '================================'
        }

        always {
            sh '''
                rm -f \
                backend.env \
                root.env
            '''
        }
    }
}