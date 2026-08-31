pipeline {
    agent any

    environment {
        DEPLOY_HOST = '3.35.199.52'
        DEPLOY_USER = 'ubuntu'
        DEPLOY_DIR = '/home/ubuntu/project'

        GIT_REPOSITORY = 'https://github.com/aame3504/cloud_pipline.git'
        GIT_BRANCH = 'main'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }


        stage('Check Files') {
            steps {
                sh '''
                    echo "===== PROJECT FILES ====="
                    find . -maxdepth 3 -type f | sort

                    echo "===== DOCKER COMPOSE ====="
                    docker compose version
                '''
            }
        }


        stage('Prepare Environment') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'openai-api-key',
                        variable: 'OPENAI_API_KEY'
                    ),
                    string(
                        credentialsId: 'database-url',
                        variable: 'DATABASE_URL'
                    ),
                    string(
                        credentialsId: 'jwt-secret-key',
                        variable: 'JWT_SECRET_KEY'
                    )
                ]) {
                    sh '''
                        mkdir -p backend

                        {
                            printf 'OPENAI_API_KEY=%s\\n' "$OPENAI_API_KEY"
                            printf 'DATABASE_URL=%s\\n' "$DATABASE_URL"
                            printf 'JWT_SECRET_KEY=%s\\n' "$JWT_SECRET_KEY"
                            printf 'AWS_REGION=ap-northeast-2\\n'
                            printf 'S3_BUCKET_NAME=aame-s3-pipeline\\n'
                            printf 'S3_IMAGE_PREFIX=images/\\n'
                            printf 'REDIS_URL=redis://redis:6379/0\\n'
                        } > backend/.env
                    '''
                }
            }
        }


        stage('Build Test') {
            steps {
                sh '''
                    echo "===== DOCKER COMPOSE CONFIG TEST ====="

                    docker compose config > /dev/null

                    echo "DOCKER COMPOSE CONFIG OK"
                '''
            }
        }


        stage('Deploy AWS') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'ea5cfc92-f35f-4e56-bcdc-cee6c35d09c8',
                        variable: 'SSH_KEY'
                    )
                ]) {
                    sh '''
                        chmod 600 "$SSH_KEY"

                        ssh \
                            -i "$SSH_KEY" \
                            -o StrictHostKeyChecking=no \
                            "$DEPLOY_USER@$DEPLOY_HOST" \
                            "
                            set -e

                            if [ ! -d '$DEPLOY_DIR/.git' ]; then
                                rm -rf '$DEPLOY_DIR'

                                git clone \
                                    --branch '$GIT_BRANCH' \
                                    '$GIT_REPOSITORY' \
                                    '$DEPLOY_DIR'
                            fi

                            cd '$DEPLOY_DIR'

                            git fetch origin

                            git reset \
                                --hard \
                                'origin/$GIT_BRANCH'

                            mkdir -p backend
                            "

                        scp \
                            -i "$SSH_KEY" \
                            -o StrictHostKeyChecking=no \
                            backend/.env \
                            "$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_DIR/backend/.env"

                        ssh \
                            -i "$SSH_KEY" \
                            -o StrictHostKeyChecking=no \
                            "$DEPLOY_USER@$DEPLOY_HOST" \
                            "
                            set -e

                            cd '$DEPLOY_DIR'

                            docker compose down \
                                --remove-orphans

                            docker compose up \
                                -d \
                                --build

                            docker image prune \
                                -f

                            echo '===== CONTAINERS ====='

                            docker compose ps
                            "
                    '''
                }
            }
        }


        stage('Health Check') {
            steps {
                sh '''
                    echo "Waiting for application startup..."

                    sleep 15

                    curl \
                        --fail \
                        --silent \
                        --show-error \
                        "http://$DEPLOY_HOST/" \
                        > /dev/null

                    echo "FRONTEND HEALTH CHECK OK"

                    curl \
                        --fail \
                        --silent \
                        --show-error \
                        "http://$DEPLOY_HOST/docs" \
                        > /dev/null

                    echo "BACKEND HEALTH CHECK OK"
                '''
            }
        }


        stage('Redis Check') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'ea5cfc92-f35f-4e56-bcdc-cee6c35d09c8',
                        variable: 'SSH_KEY'
                    )
                ]) {
                    sh '''
                        chmod 600 "$SSH_KEY"

                        ssh \
                            -i "$SSH_KEY" \
                            -o StrictHostKeyChecking=no \
                            "$DEPLOY_USER@$DEPLOY_HOST" \
                            "
                            cd '$DEPLOY_DIR'

                            docker compose exec \
                                -T \
                                redis \
                                redis-cli \
                                ping
                            "
                    '''
                }
            }
        }
    }


    post {
        success {
            echo 'AWS DEPLOY SUCCESS'
        }

        failure {
            echo 'AWS DEPLOY FAILED'
        }

        always {
            sh '''
                rm -f backend/.env
            '''
        }
    }
}