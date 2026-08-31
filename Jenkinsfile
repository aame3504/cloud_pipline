pipeline {
    agent any

    environment {
        AWS_HOST = '3.35.199.52'
        AWS_USER = 'ubuntu'

        PROJECT_DIR = '/home/ubuntu/project'
        IMAGE_DIR = '/home/ubuntu/image-rag-data/images'

        GITHUB_REPO = 'https://github.com/aame3504/cloud_pipline.git'
        GITHUB_BRANCH = 'main'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
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
                withCredentials([
                    string(
                        credentialsId: 'openai-api-key',
                        variable: 'OPENAI_API_KEY'
                    )
                ]) {
                    sh '''
                        set +x

                        printf 'OPENAI_API_KEY=%s\\n' \
                            "$OPENAI_API_KEY" \
                            > backend/.env

                        printf 'IMAGE_HOST_PATH=%s\\n' \
                            "$IMAGE_DIR" \
                            > .env

                        set -x

                        docker compose config

                        echo "================================"
                        echo "Docker Compose configuration OK"
                        echo "================================"
                    '''
                }
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
                            ssh \
                                -o StrictHostKeyChecking=no \
                                ${AWS_USER}@${AWS_HOST} \
                                "
                                    mkdir -p ${PROJECT_DIR}
                                    mkdir -p ${IMAGE_DIR}

                                    if [ ! -d '${PROJECT_DIR}/.git' ]; then
                                        rm -rf ${PROJECT_DIR}

                                        git clone \
                                            -b ${GITHUB_BRANCH} \
                                            ${GITHUB_REPO} \
                                            ${PROJECT_DIR}
                                    fi
                                "
                        '''

                        sh '''
                            ssh \
                                -o StrictHostKeyChecking=no \
                                ${AWS_USER}@${AWS_HOST} \
                                "
                                    cd ${PROJECT_DIR}

                                    git fetch origin

                                    git reset \
                                        --hard \
                                        origin/${GITHUB_BRANCH}

                                    mkdir -p ${IMAGE_DIR}
                                "
                        '''

                        sh '''
                            set +x

                            printf 'OPENAI_API_KEY=%s\\n' \
                                "$OPENAI_API_KEY" \
                                > backend.env

                            printf 'IMAGE_HOST_PATH=%s\\n' \
                                "$IMAGE_DIR" \
                                > root.env

                            set -x
                        '''

                        sh '''
                            scp \
                                -o StrictHostKeyChecking=no \
                                backend.env \
                                ${AWS_USER}@${AWS_HOST}:${PROJECT_DIR}/backend/.env

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
                            ssh \
                                -o StrictHostKeyChecking=no \
                                ${AWS_USER}@${AWS_HOST} \
                                "
                                    cd ${PROJECT_DIR}

                                    docker compose down \
                                        --remove-orphans

                                    docker compose up \
                                        -d \
                                        --build

                                    docker image prune \
                                        -f

                                    docker compose ps
                                "
                        '''
                    }
                }
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    echo "================================"
                    echo "Waiting for application"
                    echo "================================"

                    sleep 10

                    curl \
                        --fail \
                        --retry 10 \
                        --retry-delay 3 \
                        --retry-connrefused \
                        http://${AWS_HOST}/

                    echo ""
                    echo "================================"
                    echo "Health Check OK"
                    echo "================================"
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
                    root.env \
                    backend/.env \
                    .env
            '''
        }
    }
}