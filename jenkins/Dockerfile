FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update \
    && apt-get install -y \
        ca-certificates \
        curl \
        git \
        openssh-client \
        docker.io \
        docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -f docker \
    && usermod -aG docker jenkins

USER jenkins